#!/usr/bin/env python3
"""Read-only per-slide editability inventory. Not a visual or rendering validator."""
import argparse
import hashlib
import json
from pathlib import Path
import posixpath
import sys
import xml.etree.ElementTree as ET
import zipfile

NS = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
      'c': 'http://schemas.openxmlformats.org/drawingml/2006/chart'}


def audit(deck, sources, threshold):
    with zipfile.ZipFile(deck) as z:
        def xml(part):
            return ET.fromstring(z.read(part))

        def rels(part):
            folder, filename = posixpath.split(part)
            relpart = posixpath.join(folder, '_rels', filename + '.rels')
            if relpart not in z.namelist():
                return {}
            result = {}
            for r in xml(relpart):
                if r.get('TargetMode') == 'External':
                    continue
                target = r.attrib['Target']
                target = target.lstrip('/') if target.startswith('/') else posixpath.normpath(posixpath.join(folder, target))
                result[r.attrib['Id']] = (target, r.get('Type', '').rsplit('/', 1)[-1])
            return result

        presentation = xml('ppt/presentation.xml')
        size = presentation.find('p:sldSz', NS)
        if size is None:
            raise ValueError('missing presentation slide size')
        sw, sh = int(size.attrib['cx']), int(size.attrib['cy'])
        if min(sw, sh) <= 0:
            raise ValueError('invalid slide size')
        relationships = rels('ppt/presentation.xml')
        pages = []
        for i, sid in enumerate(presentation.findall('p:sldIdLst/p:sldId', NS), 1):
            part, _ = relationships[sid.attrib['{' + NS['r'] + '}id']]
            page = xml(part)
            parent = {child: node for node in page.iter() for child in node}
            shapes, pictures = page.findall('.//p:sp', NS), page.findall('.//p:pic', NS)
            texts = []
            for shape in shapes:
                paragraphs = [''.join(n.text or '' for n in p.findall('.//a:t', NS))
                              for p in shape.findall('p:txBody/a:p', NS)]
                value = '\n'.join(paragraphs).strip()
                if value:
                    texts.append(value)
            flags, image_info = [], []
            for pic in pictures:
                props = pic.find('p:nvPicPr/p:cNvPr', NS)
                name = props.get('name', '') if props is not None else ''
                grouped = False
                ancestor = parent.get(pic)
                while ancestor is not None:
                    if ancestor.tag == '{' + NS['p'] + '}grpSp':
                        grouped = True
                    ancestor = parent.get(ancestor)
                extent = pic.find('p:spPr/a:xfrm/a:ext', NS)
                info = {'name': name, 'grouped': grouped}
                if grouped:
                    flags.append({'kind': 'grouped_image_geometry_not_resolved', 'name': name})
                elif extent is None:
                    flags.append({'kind': 'image_geometry_unknown', 'name': name})
                else:
                    w, h = int(extent.get('cx', 0)), int(extent.get('cy', 0))
                    info['sizeFraction'] = [round(w / sw, 4), round(h / sh, 4)]
                    if w >= sw * threshold and h >= sh * threshold:
                        flags.append({'kind': 'near_full_slide_image', 'name': name})
                image_info.append(info)
            # Inspect inherited backgrounds, not every unused master in the package.
            inherited, seen = [part], set()
            while inherited:
                current = inherited.pop()
                if current in seen:
                    continue
                seen.add(current)
                tree = xml(current)
                bg = tree.find('p:cSld/p:bg', NS)
                if bg is not None and bg.find('.//a:blip', NS) is not None:
                    flags.append({'kind': 'image_background', 'part': current})
                if bg is not None and bg.find('p:bgRef', NS) is not None:
                    flags.append({'kind': 'theme_background_not_resolved', 'part': current})
                if bg is not None:
                    continue  # An explicit background overrides inherited backgrounds.
                for target, kind in rels(current).values():
                    if kind in ('slideLayout', 'slideMaster'):
                        inherited.append(target)
            tables = page.findall('.//a:tbl', NS)
            table_text = [''.join(n.text or '' for n in cell.findall('.//a:t', NS))
                          for table in tables for cell in table.findall('a:tr/a:tc', NS)]
            pages.append({'slide': i, 'part': part, 'nativeTextObjects': len(texts),
                          'shapes': len(shapes), 'connectors': len(page.findall('.//p:cxnSp', NS)),
                          'images': len(pictures), 'tables': len(tables),
                          'chartReferences': len(page.findall('.//c:chart', NS)),
                          'text': texts, 'tableCellText': table_text,
                          'imageGeometry': image_info, 'flags': flags})
        source_hashes = {hashlib.sha256(Path(f).read_bytes()).hexdigest(): str(f) for f in sources}
        matches = []
        for media in z.namelist():
            if media.startswith('ppt/media/') and not media.endswith('/'):
                digest = hashlib.sha256(z.read(media)).hexdigest()
                if digest in source_hashes:
                    matches.append({'media': media, 'source': source_hashes[digest]})
        return {'file': str(Path(deck).resolve()), 'slideSizeEmu': [sw, sh],
                'slideCount': len(pages), 'slides': pages, 'exactSourceMatches': matches,
                'limits': 'Counts and heuristic flags only. Does not detect all rasterized text, ghosting, text fit, or visual fidelity. Grouped transforms and theme backgrounds require separate review.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pptx', type=Path)
    parser.add_argument('--source', type=Path, action='append', default=[])
    parser.add_argument('--expected-slides', type=int)
    parser.add_argument('--require-native-text', action='store_true')
    parser.add_argument('--forbid-full-slide-images', action='store_true')
    parser.add_argument('--full-image-threshold', type=float, default=0.85)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    if not 0 < args.full_image_threshold <= 1:
        parser.error('--full-image-threshold must be in (0, 1]')
    if args.expected_slides is not None and args.expected_slides < 1:
        parser.error('--expected-slides must be positive')
    try:
        result = audit(args.pptx, args.source, args.full_image_threshold)
        failures = []
        if args.expected_slides is not None and result['slideCount'] != args.expected_slides:
            failures.append(f"expected {args.expected_slides} slides; found {result['slideCount']}")
        for slide in result['slides']:
            if args.require_native_text and not (slide['nativeTextObjects'] or any(slide['tableCellText'])):
                failures.append(f"slide {slide['slide']}: no native shape/table text")
            if args.forbid_full_slide_images:
                for flag in slide['flags']:
                    if flag['kind'] in ('near_full_slide_image', 'image_background'):
                        failures.append(f"slide {slide['slide']}: {flag['kind']}")
        result['gateFailures'] = failures
        result['gateStatus'] = 'failed' if failures else 'passed'
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            print(json.dumps({'report': str(args.report.resolve()), 'slideCount': result['slideCount'],
                              'gateStatus': result['gateStatus'], 'gateFailures': failures,
                              'flagCount': sum(len(s['flags']) for s in result['slides']),
                              'exactSourceMatches': len(result['exactSourceMatches'])}, ensure_ascii=False))
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if failures else 0
    except (OSError, ValueError, KeyError, ET.ParseError, zipfile.BadZipFile) as exc:
        print(f'audit_pptx: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
