import json
import time
from typing import Any, Dict

from behave import when, then
from allure_commons._allure import attach
from allure_commons.types import AttachmentType
import websocket  # type: ignore


@when("I connect to the market WebSocket")
def step_connect_ws(context):
    ws_market_url = context.cfg["ws_market_url"]
    context.ws = websocket.create_connection(ws_market_url, timeout=10)
    attach(ws_market_url, name="WS Market URL", attachment_type=AttachmentType.TEXT)


@when('I subscribe to the "{instrument_name}" book channel with depth "{depth}"')
def step_subscribe_book_with_depth(context, instrument_name: str, depth: str):
    msg = {
        "id": "1",
        "method": "subscribe",
        "params": {
            "channels": [f"book.{instrument_name}.{depth}"]
        }
    }
    context.ws.send(json.dumps(msg))
    attach(json.dumps(msg, indent=2), name="Sent message", attachment_type=AttachmentType.JSON)


@when("I send this JSON message:")
def step_send_json_message(context):
    msg = json.loads(context.text)
    context.ws.send(json.dumps(msg))
    attach(json.dumps(msg, indent=2), name="Sent message", attachment_type=AttachmentType.JSON)


@then("I should receive a message acknowledging subscription or data")
def step_receive_message(context):
    end = time.time() + 15.0
    payload = None
    while time.time() < end:
        try:
            raw = context.ws.recv()
            if raw:
                payload = json.loads(raw)
                break
        except websocket.WebSocketTimeoutException:
            pass
    assert payload is not None, "Did not receive any message within timeout"
    attach(json.dumps(payload, indent=2), name="Received message", attachment_type=AttachmentType.JSON)
    assert isinstance(payload, dict)
    assert any(k in payload for k in ("result", "channel", "data", "params"))
    context.ws.close()

