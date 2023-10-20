from enum import Enum


class Modes(str, Enum):
    development = "development"
    staging = "staging"
    production = "production"


class Tags(str, Enum):
    server_health = "Server Health"
