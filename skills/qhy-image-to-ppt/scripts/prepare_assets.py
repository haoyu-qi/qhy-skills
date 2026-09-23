#!/usr/bin/env python3
"""Crop source pixels without upscaling. Requires Pillow."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True, type=Path)
    parser.add_argument('--manifest', required=True, type=Path)
    parser.add_argument('--output-dir', required=True, type=Path)
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()
    try:
        from PIL import Image, ImageOps
        spec = json.loads(args.manifest.read_text(encoding='utf-8'))
        if not isinstance(spec, dict):
            raise ValueError('manifest must be an object')
        crops = spec.get('crops')
        if not isinstance(crops, list) or not crops:
            raise ValueError('manifest.crops must be a nonempty list')
        with Image.open(args.source) as original:
            im = ImageOps.exif_transpose(original)
            im.load()
            width, height = im.size
            ids, checked = set(), []
            for entry in crops:
                if not isinstance(entry, dict):
                    raise ValueError('each crop must be an object')
                ident, box = entry.get('id'), entry.get('box')
                if not isinstance(ident, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,95}', ident):
                    raise ValueError('crop id must be 1–96 ASCII letters/digits/underscores/hyphens, starting alphanumeric')
                if ident in ids:
                    raise ValueError(f'duplicate crop id: {ident}')
                ids.add(ident)
                if not isinstance(box, list) or len(box) != 4 or any(type(n) is not int for n in box):
                    raise ValueError(f'{ident}: box must contain four integer pixel coordinates')
                x, y, w, h = box
                if x < 0 or y < 0 or w <= 0 or h <= 0 or x + w > width or y + h > height:
                    raise ValueError(f'{ident}: crop {box} is outside oriented source {width}x{height}')
                checked.append((ident, box, args.output_dir / f'{ident}.png'))
            targets = [p for _, _, p in checked] + [args.output_dir / 'assets.json']
            if not args.overwrite:
                existing = [str(p) for p in targets if p.exists()]
                if existing:
                    raise ValueError(f'refusing overwrite: {existing[0]} (use a new directory or --overwrite)')
            args.output_dir.mkdir(parents=True, exist_ok=True)
            assets = []
            for ident, box, target in checked:
                x, y, w, h = box
                tile = im.crop((x, y, x + w, y + h))
                if tile.mode not in ('RGB', 'RGBA', 'L', 'LA'):
                    tile = tile.convert('RGBA' if 'transparency' in tile.info else 'RGB')
                tile.save(target, format='PNG')
                assets.append({'id': ident, 'sourceBox': box, 'file': target.name,
                               'width': w, 'height': h,
                               'sha256': hashlib.sha256(target.read_bytes()).hexdigest()})
        report = {'source': str(args.source.resolve()),
                  'sourceSha256': hashlib.sha256(args.source.read_bytes()).hexdigest(),
                  'orientedSize': [width, height], 'upscaled': False, 'assets': assets}
        (args.output_dir / 'assets.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(json.dumps({'count': len(assets), 'manifest': str((args.output_dir / 'assets.json').resolve())}, ensure_ascii=False))
    except (ImportError, OSError, ValueError, TypeError, KeyError) as exc:
        print(f'prepare_assets: {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
