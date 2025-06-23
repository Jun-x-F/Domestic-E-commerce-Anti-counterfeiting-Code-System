from pathlib import Path
from sqlalchemy import create_engine, text

from anticounterfeiting.generator import generate_code, generate_codes


def test_generate_code():
    code = generate_code('secret')
    assert len(code) > 32


def test_generate_codes(tmp_path: Path):
    db = tmp_path / 'db.sqlite'
    engine = create_engine(f'sqlite:///{db}')
    generate_codes('SPU1', 'online', 2, str(engine.url), 'secret')
    with engine.connect() as conn:
        count = conn.execute(text('SELECT COUNT(*) FROM spu_channel_code')).scalar()
    assert count == 2
