import os
from pathlib import Path
from pydantic import BaseModel
from typing import Optional


class AppConfig(BaseModel):
    app_name: str = "RTS Game Designer"
    version: str = "1.0.0"
    window_width: int = 1400
    window_height: int = 900
    auto_save: bool = True
    auto_save_interval: int = 30000

    data_dir: str = str(Path.home() / "RTS_Game_Designer_Data")
    excel_file: str = "game_data.xlsx"
    images_dir: str = "hero_images"
    exports_dir: str = "exports"
    config_file: str = "config.json"

    window_state: dict = {}
    last_opened_project: str = ""
    recent_projects: list = []


DEFAULT_CONFIG = AppConfig()


def get_config_path() -> Path:
    return Path(DEFAULT_CONFIG.data_dir) / DEFAULT_CONFIG.config_file


def load_config() -> AppConfig:
    config_path = get_config_path()
    if config_path.exists():
        try:
            return AppConfig.model_validate_json(config_path.read_text())
        except Exception:
            pass
    return DEFAULT_CONFIG


def save_config(config: AppConfig) -> None:
    config_path = get_config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(config.model_dump_json(indent=2))


def ensure_directories(config: AppConfig) -> None:
    Path(config.data_dir).mkdir(parents=True, exist_ok=True)
    (Path(config.data_dir) / config.images_dir).mkdir(parents=True, exist_ok=True)
    (Path(config.data_dir) / config.exports_dir).mkdir(parents=True, exist_ok=True)