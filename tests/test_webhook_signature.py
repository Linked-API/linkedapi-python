from __future__ import annotations

import hashlib
import hmac
from typing import Any

import pytest

from linkedapi import (
    WEBHOOK_SIGNATURE_HEADER,
    WEBHOOK_SIGNATURE_TIMESTAMP_HEADER,
    verify_webhook_signature,
)

SECRET = "000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f"
TIMESTAMP = "1700000000"
NOW_SECONDS = 1700000000
ASCII_BODY = '{"id":"event-1","type":"webhook.test","data":{"message":"Hello"}}'
ASCII_SIGNATURE = "8f93c19766fe42f27da56fcb5ae11a909c406683ccc0766bd29edc52c71fd209"
UNICODE_BODY = '{"id":"event-2","type":"webhook.test","data":{"message":"Zoë ♥ 日本"}}'
UNICODE_SIGNATURE = "87f5bc51d542ce4d8b61350b35807420dce7b3473bd7ecec87211b544c299c69"
PARAMS: dict[str, Any] = {
    "raw_body": ASCII_BODY,
    "timestamp": TIMESTAMP,
    "signature": ASCII_SIGNATURE,
    "secret": SECRET,
    "now_seconds": NOW_SECONDS,
}


@pytest.mark.parametrize(
    ("raw_body", "signature"),
    [
        (body, signature)
        for text, signature in [(ASCII_BODY, ASCII_SIGNATURE), (UNICODE_BODY, UNICODE_SIGNATURE)]
        for body in [text, text.encode(), bytearray(text.encode()), memoryview(text.encode())]
    ],
)
def test_documented_vectors(raw_body: str | bytes | bytearray | memoryview, signature: str) -> None:
    assert verify_webhook_signature(**(PARAMS | {"raw_body": raw_body, "signature": signature}))


def test_hex_decoded_secret_signature_is_rejected() -> None:
    assert not verify_webhook_signature(
        **(
            PARAMS
            | {"signature": "cf8a7cbd4da0130448492ced3d1aaffd608738b7fff2623e27eaecd4dd54a236"}
        )
    )


@pytest.mark.parametrize("raw_body", [ASCII_BODY + " ", ASCII_BODY.replace("Hello", "Forged")])
def test_tampered_body(raw_body: str) -> None:
    assert not verify_webhook_signature(**(PARAMS | {"raw_body": raw_body}))


def test_tampered_signature() -> None:
    assert not verify_webhook_signature(**(PARAMS | {"signature": "0" + ASCII_SIGNATURE[1:]}))


def test_wrong_secret() -> None:
    assert not verify_webhook_signature(**(PARAMS | {"secret": SECRET + "x"}))


@pytest.mark.parametrize(
    "signature",
    [
        None,
        [],
        [ASCII_SIGNATURE],
        "",
        "a" * 63,
        "a" * 65,
        "g" * 64,
        ASCII_SIGNATURE.upper(),
        ASCII_SIGNATURE + "\n",
        "sha256=" + ASCII_SIGNATURE,
    ],
)
def test_signature_shape(signature: Any) -> None:
    assert not verify_webhook_signature(**(PARAMS | {"signature": signature}))


@pytest.mark.parametrize("offset", [-300, 300])
def test_default_tolerance_boundary(offset: int) -> None:
    assert verify_webhook_signature(**(PARAMS | {"now_seconds": NOW_SECONDS + offset}))


@pytest.mark.parametrize("offset", [-301, 301])
def test_default_tolerance_both_directions(offset: int) -> None:
    assert not verify_webhook_signature(**(PARAMS | {"now_seconds": NOW_SECONDS + offset}))


@pytest.mark.parametrize(
    ("offset", "expected"), [(-60, True), (60, True), (-61, False), (61, False)]
)
def test_custom_tolerance(offset: int, expected: bool) -> None:
    assert (
        verify_webhook_signature(
            **(PARAMS | {"now_seconds": NOW_SECONDS + offset, "tolerance_seconds": 60})
        )
        is expected
    )


def test_default_clock(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("linkedapi.webhooks.signature.time.time", lambda: NOW_SECONDS)
    assert verify_webhook_signature(**(PARAMS | {"now_seconds": None}))
    monkeypatch.setattr("linkedapi.webhooks.signature.time.time", lambda: NOW_SECONDS + 301)
    assert not verify_webhook_signature(**(PARAMS | {"now_seconds": None}))


def test_integer_timestamp() -> None:
    assert verify_webhook_signature(**(PARAMS | {"timestamp": NOW_SECONDS}))


@pytest.mark.parametrize(
    "timestamp",
    [
        True,
        False,
        1700000000.0,
        1700000000.5,
        "1700000000.5",
        "1.7e9",
        " 1700000000",
        "1700000000\n",
        "+1700000000",
        "\u0661\u0667" + "\u0660" * 8,
        "",
        None,
        [TIMESTAMP],
    ],
)
def test_invalid_timestamp_even_with_matching_hmac(timestamp: Any) -> None:
    signature = hmac.new(
        SECRET.encode(), f"{timestamp}.{ASCII_BODY}".encode(), hashlib.sha256
    ).hexdigest()
    now_seconds = int(timestamp) if isinstance(timestamp, (bool, int, float)) else NOW_SECONDS
    assert not verify_webhook_signature(
        **(PARAMS | {"timestamp": timestamp, "signature": signature, "now_seconds": now_seconds})
    )


@pytest.mark.parametrize("now_seconds", [True, False, "1700000000", [], float("nan"), float("inf")])
def test_invalid_clock(now_seconds: Any) -> None:
    assert not verify_webhook_signature(**(PARAMS | {"now_seconds": now_seconds}))


@pytest.mark.parametrize(
    "tolerance_seconds", [True, False, None, [], -1, float("nan"), float("inf")]
)
def test_invalid_tolerance(tolerance_seconds: Any) -> None:
    assert not verify_webhook_signature(**(PARAMS | {"tolerance_seconds": tolerance_seconds}))


@pytest.mark.parametrize(
    ("field", "value"),
    [
        (field, value)
        for field in [
            "raw_body",
            "timestamp",
            "signature",
            "secret",
            "now_seconds",
            "tolerance_seconds",
        ]
        for value in [object(), {}, [], True, float("nan"), float("inf")]
    ]
    + [
        (field, None)
        for field in ["raw_body", "timestamp", "signature", "secret", "tolerance_seconds"]
    ]
    + [(field, 1.5) for field in ["raw_body", "timestamp", "signature", "secret"]],
)
def test_malformed_inputs_never_raise(field: str, value: Any) -> None:
    assert verify_webhook_signature(**(PARAMS | {field: value})) is False


def test_finite_fractional_clock_and_tolerance() -> None:
    assert verify_webhook_signature(
        **(PARAMS | {"now_seconds": NOW_SECONDS + 0.5, "tolerance_seconds": 1.5})
    )


@pytest.mark.parametrize(
    ("offset", "expected"),
    [
        (-1.25, True),
        (1.25, True),
        (-1.5, True),
        (1.5, True),
        (-1.5001, False),
        (1.5001, False),
    ],
)
def test_fractional_tolerance_boundaries(offset: float, expected: bool) -> None:
    assert (
        verify_webhook_signature(
            **(PARAMS | {"now_seconds": NOW_SECONDS + offset, "tolerance_seconds": 1.5})
        )
        is expected
    )


def test_invalid_utf8_string_never_raises() -> None:
    assert not verify_webhook_signature(**(PARAMS | {"raw_body": "\ud800"}))


def test_released_memoryview_never_raises() -> None:
    raw_body = memoryview(ASCII_BODY.encode())
    raw_body.release()
    assert not verify_webhook_signature(**(PARAMS | {"raw_body": raw_body}))


def test_byte_view_preserves_bytes() -> None:
    body = memoryview(b"x" + UNICODE_BODY.encode() + b"y")[1:-1]
    assert verify_webhook_signature(**(PARAMS | {"raw_body": body, "signature": UNICODE_SIGNATURE}))


def test_wire_header_names() -> None:
    assert WEBHOOK_SIGNATURE_HEADER == "linked-api-signature"
    assert WEBHOOK_SIGNATURE_TIMESTAMP_HEADER == "linked-api-signature-timestamp"
