from anticounterfeiting.generator import generate_codes
from anticounterfeiting.tasks import render_qr


def main():
    """Generate a few demo codes and render their QR images."""
    db_url = "sqlite:///demo.sqlite"
    codes = generate_codes("SPU_DEMO", "online", 2, db_url, "secret")
    for code in codes:
        url = f"https://verify.domain.com/check.html?code={code}"
        path = render_qr(code, url, "qrcodes")
        print(f"{code} -> {path}")


if __name__ == "__main__":
    main()
