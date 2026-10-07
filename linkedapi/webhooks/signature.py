from __future__ import annotations

import hashlib
import hmac
import math
import re
import time


def verify_webhook_signature(
    *,
    raw_body: str | bytes | bytearray | memoryview,
    timestamp: str | int | list[str] | None,
    signature: str | list[str] | None,
    secret: str | None,
    now_seconds: float | None = None,
    tolerance_seconds: float = 300,
) -> bool:
    """Verify a signed webhook before parsing its raw request body.

    Use the secret as literal UTF-8 text, never hex-decode it. Timestamps are integer Unix
    seconds. The default tolerance is 300 seconds in either direction and must be finite
    and non-negative. Inject now_seconds to check a stored delivery at a chosen time.
    Malformed inputs return False.

    Example:
        verify_webhook_signature(
            raw_body=request.body,
            timestamp=request.headers.get(WEBHOOK_SIGNATURE_TIMESTAMP_HEADER),
            signature=request.headers.get(WEBHOOK_SIGNATURE_HEADER),
            secret=secret,
        )
    """
    try:
        if (
            not isinstance(signature, str)
            or re.fullmatch(r"[0-9a-f]{64}", signature) is None
            or not isinstance(secret, str)
            or not secret
            or not isinstance(raw_body, (str, bytes, bytearray, memoryview))
        ):
            return False

        if isinstance(timestamp, bool):
            return False
        if isinstance(timestamp, str):
            if re.fullmatch(r"[0-9]+", timestamp) is None:
                return False
            sent_at = int(timestamp)
        elif isinstance(timestamp, int):
            sent_at = timestamp
        else:
            return False

        if now_seconds is None:
            now_seconds = int(time.time())
        if (
            isinstance(now_seconds, bool)
            or not isinstance(now_seconds, (int, float))
            or not math.isfinite(now_seconds)
            or isinstance(tolerance_seconds, bool)
            or not isinstance(tolerance_seconds, (int, float))
            or not math.isfinite(tolerance_seconds)
            or tolerance_seconds < 0
            or abs(now_seconds - sent_at) > tolerance_seconds
        ):
            return False

        body_bytes = raw_body.encode("utf-8") if isinstance(raw_body, str) else bytes(raw_body)
        expected = hmac.new(secret.encode("utf-8"), digestmod=hashlib.sha256)
        expected.update(f"{timestamp}.".encode())
        expected.update(body_bytes)
        return hmac.compare_digest(expected.hexdigest(), signature)
    except Exception:
        return False
