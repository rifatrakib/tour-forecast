import json
from functools import lru_cache
from typing import Any, Dict, Tuple, Type

from decouple import config
from pydantic.fields import FieldInfo
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict

from api.utils.enums import Modes


@lru_cache()
def read_secrets() -> Dict[str, Any]:
    mode = config("MODE", default="development")
    with open(f"secrets/{mode}.json", "r") as reader:
        secrets = json.loads(reader.read())
    return secrets


class SettingsSource(PydanticBaseSettingsSource):
    def get_field_value(self, field: FieldInfo, field_name: str) -> Tuple[Any, str, bool]:
        secrets = read_secrets()
        field_value = secrets.get(field_name)
        return field_value, field_name, False

    def prepare_field_value(self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool) -> Any:
        return value

    def __call__(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {}

        for name, field in self.settings_cls.model_fields.items():
            value, key, is_complex = self.get_field_value(field, name)
            value = self.prepare_field_value(name, field, value, is_complex)
            if value is not None:
                d[key] = value

        return d


class BaseConfig(BaseSettings):
    APP_NAME: str
    MODE: Modes

    # SQL Database Configurations
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    # PGAdmin Configurations
    PGADMIN_DEFAULT_EMAIL: str
    PGADMIN_DEFAULT_PASSWORD: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="forbid",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return init_settings, env_settings, dotenv_settings, SettingsSource(settings_cls)

    @property
    def RDS_URI(self) -> str:
        username = self.POSTGRES_USER
        password = self.POSTGRES_PASSWORD
        host = self.POSTGRES_HOST
        port = self.POSTGRES_PORT
        db_name = self.POSTGRES_DB
        return f"postgresql+asyncpg://{username}:{password}@{host}:{port}/{db_name}"
