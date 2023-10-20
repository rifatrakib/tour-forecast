from functools import lru_cache
from typing import Type

from decouple import config

from api.config.environments import BaseConfig
from api.config.environments.development import DevelopmentConfig
from api.config.environments.production import ProductionConfig
from api.config.environments.staging import StagingConfig
from api.utils.enums import Modes


class SettingsFactory:
    def __init__(self, mode: str):
        self.mode = mode

    def __call__(self) -> Type[BaseConfig]:
        if self.mode == Modes.staging:  # pragma: no cover
            return StagingConfig()
        elif self.mode == Modes.production:
            return ProductionConfig()
        else:  # pragma: no cover
            return DevelopmentConfig()


@lru_cache()
def get_settings() -> Type[BaseConfig]:
    factory = SettingsFactory(mode=config("MODE", default="development"))
    return factory()


settings: Type[BaseConfig] = get_settings()
