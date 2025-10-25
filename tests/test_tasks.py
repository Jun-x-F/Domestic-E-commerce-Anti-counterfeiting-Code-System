from pathlib import Path

from anticounterfeiting.tasks import render_qr


def test_render_qr(tmp_path: Path):
    output = render_qr('code123', 'http://example.com?c=code123', str(tmp_path))
    assert Path(output).exists()
