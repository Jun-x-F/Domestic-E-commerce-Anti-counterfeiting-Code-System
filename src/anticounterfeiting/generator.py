import uuid
import hmac
import hashlib
from datetime import datetime
from typing import Iterable
from sqlalchemy import (create_engine, MetaData, Table, Column, Integer, String,
                        DateTime, insert)


def generate_code(secret: str) -> str:
    """Generate a unique code with an HMAC signature."""
    base = uuid.uuid4().hex
    signature = hmac.new(secret.encode(), base.encode(), hashlib.sha256).hexdigest()[:8]
    return f"{base}{signature}"


def init_table(metadata: MetaData) -> Table:
    """Return the spu_channel_code table definition."""
    return Table(
        "spu_channel_code",
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("spu", String(64), nullable=False),
        Column("channel", String(64), nullable=False),
        Column("code", String(80), nullable=False, unique=True),
        Column("url", String(255), nullable=False),
        Column("qr_path", String(255)),
        Column("created_at", DateTime, nullable=False),
        Column("updated_at", DateTime, nullable=False),
    )


def generate_codes(spu: str, channel: str, count: int, db_url: str, secret: str) -> Iterable[str]:
    """Generate multiple codes for an SPU and channel and store them."""
    engine = create_engine(db_url)
    metadata = MetaData()
    table = init_table(metadata)
    metadata.create_all(engine)

    codes = []
    with engine.begin() as conn:
        for _ in range(count):
            code = generate_code(secret)
            url = f"https://verify.domain.com/check.html?code={code}"
            now = datetime.utcnow()
            conn.execute(
                insert(table).values(
                    spu=spu,
                    channel=channel,
                    code=code,
                    url=url,
                    created_at=now,
                    updated_at=now,
                )
            )
            codes.append(code)
    return codes
