import json
import os
from pathlib import Path
from typing import Any, Dict


def load_config(env_name: str | None = None) -> Dict[str, Any]:
    """
    Load configuration for the selected environment.
    Environment can be provided via function argument, pytest --env, or TEST_ENV env var.
    Defaults to UAT.
    """
    selected_env = (env_name or os.getenv("TEST_ENV") or "UAT").upper()

    config_path = Path(__file__).resolve().parent.parent / "config" / "env.json"
    with config_path.open("r", encoding="utf-8") as f:
        all_envs = json.load(f)

    if selected_env not in all_envs:
        raise ValueError(f"Unknown environment '{selected_env}'. Valid: {', '.join(all_envs.keys())}")

    config = dict(all_envs[selected_env])  # copy to avoid mutating loaded data
    # Normalize/enrich fields for downstream usage
    config["selected_env"] = selected_env
    config["name"] = config.get("name", selected_env)
    # Prefer explicit ws_url; otherwise default to market URL, then user URL
    if "ws_url" not in config:
        ws_fallback = config.get("ws_market_url") or config.get("ws_user_url")
        if ws_fallback:
            config["ws_url"] = ws_fallback

    # Allow API key override via environment variable for security
    # Only relevant for PROD, but harmless elsewhere
    env_api_key = os.getenv("API_KEY")
    if env_api_key:
        config["api_key"] = env_api_key
    return config


def allure_results_dir() -> Path:
    """
    Resolve Allure results directory. Can be overridden by ALLURE_RESULTS_DIR env var.
    """
    dirname = os.getenv("ALLURE_RESULTS_DIR", "allure-results")
    return Path(dirname).resolve()

