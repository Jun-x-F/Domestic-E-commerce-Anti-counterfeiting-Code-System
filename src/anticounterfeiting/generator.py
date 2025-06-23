"""Utilities for creating and storing anti-counterfeiting codes."""

import uuid
import hmac
import hashlib
from datetime import datetime
from typing import Iterable
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    DateTime,
    insert,
)


def generate_code(secret: str) -> str:
    """Return a single random code signed with ``secret``.

    The code is a UUID4 hex string followed by the first eight characters of an
    HMAC-SHA256 signature.  This signature allows simple validation on the
    verification endpoint.
    """

    base = uuid.uuid4().hex
    signature = hmac.new(secret.encode(), base.encode(), hashlib.sha256).hexdigest()[:8]
    return f"{base}{signature}"


def init_table(metadata: MetaData) -> Table:
    """Create the ``spu_channel_code`` table definition."""
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


def generate_codes(
    spu: str,
    channel: str,
    count: int,
    db_url: str,
    secret: str,
) -> Iterable[str]:
    """Generate ``count`` codes for the given SPU and channel.

    All generated codes are persisted to the database specified by ``db_url``.
    The function yields the raw codes so that callers can create QR codes or
    perform further processing.
    """

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
