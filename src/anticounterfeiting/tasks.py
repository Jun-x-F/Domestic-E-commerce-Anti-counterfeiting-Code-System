from pathlib import Path
from celery import Celery
import qrcode

app = Celery('anticounterfeiting')


@app.task
def render_qr(code: str, url: str, output_dir: str) -> str:
    """Render a QR code PNG to the output directory."""
    img = qrcode.make(url)
    output_path = Path(output_dir) / f"{code}.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path)
    return str(output_path)
