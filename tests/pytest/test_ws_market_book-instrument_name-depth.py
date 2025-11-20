import json
import time
from pathlib import Path
from typing import Dict, Any

import allure
import pytest
import websocket  # type: ignore

from utils.data_loader import load_json_file


def _recv_with_timeout(ws: websocket.WebSocket, timeout_sec: float = 10.0) -> str:
    end = time.time() + timeout_sec
    while time.time() < end:
        try:
            msg = ws.recv()
            if msg:
                return msg
        except websocket.WebSocketTimeoutException:
            pass
    raise TimeoutError(f"No message received within {timeout_sec} seconds")


@pytest.mark.ws
@pytest.mark.parametrize("case", load_json_file(Path("data/ws/market/book-instrument_name-depth.json")))
def test_ws_subscribe_book_env(case: Dict[str, Any], config: Dict[str, Any]):
    ws_market_url = config["ws_market_url"]
    subscribe_msg = case["channel_params"]

    allure.dynamic.title(f"WebSocket subscribe ({config.get('name', '')}) - {case.get('description', '')}")
    allure.attach(ws_market_url, name="WS Market URL", attachment_type=allure.attachment_type.TEXT)
    allure.attach(json.dumps(subscribe_msg, indent=2), name="Subscribe message", attachment_type=allure.attachment_type.JSON)

    ws = websocket.create_connection(ws_market_url, timeout=10)
    try:
        ws.send(json.dumps(subscribe_msg))
        raw = _recv_with_timeout(ws, timeout_sec=15.0)
        allure.attach(raw, name="Received raw message", attachment_type=allure.attachment_type.JSON)

        data = json.loads(raw)
        # Allow either immediate result/ack or a data push with channel name
        assert isinstance(data, dict)
        if "result" in data:
            assert str(data.get("id")) == str(subscribe_msg["id"])
        elif "channel" in data:
            # Some streams push data snapshots right away
            channels = subscribe_msg["params"]["channels"]
            assert any(ch in data.get("channel", "") for ch in channels)
        else:
            # Some servers wrap in 'params' or 'data'
            assert any(k in data for k in ("result", "channel", "data", "params")), f"Unexpected WS message keys: {list(data.keys())}"
    finally:
        ws.close()

