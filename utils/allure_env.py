from pathlib import Path
from typing import Dict

from .config import allure_results_dir


def write_allure_env_properties(env_info: Dict[str, str]) -> None:
    """
    Write Allure environment.properties file so the environment is shown in the report.
    """
    results_dir = allure_results_dir()
    results_dir.mkdir(parents=True, exist_ok=True)
    env_file = results_dir / "environment.properties"
    with env_file.open("w", encoding="utf-8") as f:
        for key, value in env_info.items():
            f.write(f"{key}={value}\n")

