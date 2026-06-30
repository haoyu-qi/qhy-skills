import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "qhy-draw-gif"
MODULE_PATH = SKILL_ROOT / "scripts" / "render_animated_diagram.py"


def load_renderer():
    spec = importlib.util.spec_from_file_location("render_animated_diagram", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class QhyDrawGifRendererTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.renderer = load_renderer()
        cls.spec = json.loads((SKILL_ROOT / "assets" / "default-spec.json").read_text(encoding="utf-8"))

    def test_generated_outputs_pass_contract_checks(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.renderer.write_outputs(self.spec, Path(tmp), "sample")
            checks = self.renderer.check_outputs(result, self.spec)

        self.assertEqual(result["style"], "lanshu-classic")
        self.assertTrue(checks["ok"], checks)

    def test_each_builtin_style_renders_and_passes_checks(self):
        for style_id in self.renderer.STYLE_THEMES:
            with self.subTest(style=style_id):
                with tempfile.TemporaryDirectory() as tmp:
                    result = self.renderer.write_outputs(self.spec, Path(tmp), f"sample-{style_id}", style_id=style_id)
                    checks = self.renderer.check_outputs(result, self.spec)

                self.assertEqual(result["style"], style_id)
                self.assertTrue(checks["ok"], checks)

    def test_cli_style_overrides_spec_style(self):
        spec = dict(self.spec)
        spec["style"] = "terminal-green"
        with tempfile.TemporaryDirectory() as tmp:
            spec_path = Path(tmp) / "spec.json"
            spec_path.write_text(json.dumps(spec), encoding="utf-8")
            output = subprocess.check_output(
                [
                    sys.executable,
                    str(MODULE_PATH),
                    "--spec",
                    str(spec_path),
                    "--outdir",
                    tmp,
                    "--basename",
                    "override",
                    "--style",
                    "paper-ink",
                    "--check",
                ],
                text=True,
            )

        result = json.loads(output)
        self.assertEqual(result["style"], "paper-ink")
        self.assertTrue(result["checks"]["ok"], result["checks"])

    def test_cli_list_styles_includes_five_styles(self):
        output = subprocess.check_output([sys.executable, str(MODULE_PATH), "--list-styles"], text=True)
        styles = json.loads(output)

        self.assertEqual(
            set(styles),
            {"lanshu-classic", "terminal-green", "blueprint-cyan", "warm-amber", "paper-ink"},
        )

    def test_wraps_cjk_text_without_spaces(self):
        image = Image.new("RGBA", (300, 160), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        text, _, font = self.renderer.fit_text(
            draw,
            "研究问题收敛与证据综合",
            70,
            48,
            16,
            min_size=10,
        )

        width, height = self.renderer.text_size(draw, text, font)
        self.assertLessEqual(width, self.renderer.c(70))
        self.assertLessEqual(height, self.renderer.c(48))
        self.assertIn("\n", text)

    def test_render_writes_wrapped_text_to_excalidraw(self):
        spec = json.loads(json.dumps(self.spec))
        spec["decision"]["body"] = "checkpoint confirmation required"
        with tempfile.TemporaryDirectory() as tmp:
            result = self.renderer.write_outputs(spec, Path(tmp), "sample")
            excalidraw = json.loads(Path(result["excalidraw"]).read_text(encoding="utf-8"))

        text_values = [element["text"] for element in excalidraw["elements"] if element.get("type") == "text"]
        self.assertIn("checkpoint\nconfirmation\nrequired", text_values)


if __name__ == "__main__":
    unittest.main()
