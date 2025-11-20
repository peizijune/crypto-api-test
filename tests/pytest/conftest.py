import os
from pathlib import Path
from typing import Dict, Generator

import pytest
import allure
from playwright.sync_api import Playwright, APIRequestContext, sync_playwright

from utils.config import load_config
from utils.allure_env import write_allure_env_properties


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--env", action="store", default=os.getenv("TEST_ENV", "UAT"), help="Test environment: UAT or PROD")


@pytest.fixture(scope="session")
def test_env(request: pytest.FixtureRequest) -> str:
    env = str(request.config.getoption("--env")).upper()
    return env


@pytest.fixture(scope="session")
def config(test_env: str) -> Dict:
    cfg = load_config(test_env)
    # Write Allure env info once per session
    write_allure_env_properties(
        {
            "Environment": cfg["name"],
            "REST Base URL": cfg["rest_base_url"],
            "WS Market URL": cfg["ws_market_url"],
            "WS User URL": cfg["ws_user_url"],
        }
    )
    return cfg


@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def api_context(playwright_instance: Playwright, config: Dict) -> Generator[APIRequestContext, None, None]:
    # Ensure JSON content type and optional API key for PROD
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    api_key = config.get("api_key")
    if api_key:
        headers["api_key"] = api_key

    request_context = playwright_instance.request.new_context(
        base_url=config["rest_base_url"],
        extra_http_headers=headers,
    )
    yield request_context
    request_context.dispose()

