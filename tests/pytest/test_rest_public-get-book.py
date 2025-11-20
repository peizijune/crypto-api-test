import json
from pathlib import Path

import allure
import pytest
from playwright.sync_api import APIRequestContext

from utils.data_loader import load_json_file


@pytest.mark.parametrize("case", load_json_file(Path("data/rest/public-get-candlestick.json")))
def test_get_candlestick_success(api_context: APIRequestContext, case: dict):
    path = "public/get-candlestick"
    params = case.get("request_params", {})
    allure.dynamic.title(f"REST get-candlestick - {case.get('description', '')}")
    with allure.step(f"GET {path}"):
        response = api_context.get(path, params=params)
        allure.attach(json.dumps(params, indent=2), name="Request params", attachment_type=allure.attachment_type.JSON)
    with allure.step("Validate response status"):
        assert response.ok, f"Unexpected status {response.status}: {response.text()}"
    body = response.json()
    allure.attach(json.dumps(body, indent=2), name="Response body", attachment_type=allure.attachment_type.JSON)
    with allure.step("Validate response schema basics"):
        assert isinstance(body, dict)
        # Accept common API shapes: either 'result' or 'data' key
        assert any(k in body for k in ("result", "data")), f"Unexpected body keys: {list(body.keys())}"

