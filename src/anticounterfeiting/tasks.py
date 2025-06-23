"""Celery tasks for rendering QR code images."""

from pathlib import Path
from celery import Celery
import qrcode

# Configure a minimal Celery application. In a real deployment the broker
# and backend would be configured via Celery's configuration system.
app = Celery("anticounterfeiting")


@app.task
def render_qr(code: str, url: str, output_dir: str) -> str:
    """Render ``url`` to a QR code PNG.

    Parameters
    ----------
    code:
        Code string used as the filename.
    url:
        Destination URL encoded in the QR image.
    output_dir:
        Directory where the PNG will be written.
    """

    img = qrcode.make(url)
    output_path = Path(output_dir) / f"{code}.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path)
    return str(output_path)
