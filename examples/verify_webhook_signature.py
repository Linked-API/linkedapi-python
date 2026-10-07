from __future__ import annotations

from collections.abc import Mapping

from linkedapi import (
    WEBHOOK_SIGNATURE_HEADER,
    WEBHOOK_SIGNATURE_TIMESTAMP_HEADER,
    verify_webhook_signature,
)


def verify_request(raw_body: bytes, headers: Mapping[str, str], *, secret: str | None) -> bool:
    """Pass Flask's request.get_data() or Django's request.body and request.headers."""
    return verify_webhook_signature(
        raw_body=raw_body,
        timestamp=headers.get(WEBHOOK_SIGNATURE_TIMESTAMP_HEADER),
        signature=headers.get(WEBHOOK_SIGNATURE_HEADER),
        secret=secret,
    )
