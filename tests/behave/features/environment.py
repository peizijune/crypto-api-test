import json
from typing import Any, Dict

from allure_commons._allure import attach
from allure_commons.types import AttachmentType
from playwright.sync_api import sync_playwright, Playwright, APIRequestContext

from utils.config import load_config
from utils.allure_env import write_allure_env_properties


def before_all(context) -> None:
    env_name = (getattr(context.config.userdata, "env", None) or "UAT").upper()
    cfg: Dict[str, Any] = load_config(env_name)
    context.cfg = cfg

    write_allure_env_properties(
        {
            "Environment": cfg["name"],
            "REST Base URL": cfg["rest_base_url"],
            "WS Market URL": cfg["ws_market_url"],
            "WS User URL": cfg["ws_user_url"],
        }
    )

    context._playwright: Playwright = sync_playwright().start()
    context.api_context: APIRequestContext = context._playwright.request.new_context(base_url=cfg["rest_base_url"])
    attach(json.dumps(cfg, indent=2), name="Config", attachment_type=AttachmentType.JSON)


def after_all(context) -> None:
    if getattr(context, "api_context", None):
        context.api_context.dispose()
    if getattr(context, "_playwright", None):
        context._playwright.stop()

