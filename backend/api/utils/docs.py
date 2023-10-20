from typing import Dict, List

from api.config.factory import settings
from api.utils.enums import Tags


def retrieve_api_metadata() -> Dict[str, str]:
    with open("README.md") as reader:
        description = reader.read()

    api_metadata = {
        "title": settings.APP_NAME,
        "description": description,
        "version": "0.1.0",
        "terms_of_service": "http://127.0.0.1:8000/docs",
        "contact": {
            "name": f"Maintainer: {settings.APP_NAME}",
            "url": "http://127.0.0.1:8000/docs",
            "email": settings.PGADMIN_DEFAULT_EMAIL,
        },
    }

    return api_metadata


def retrieve_tags_metadata() -> List[Dict[str, str]]:
    return [
        {
            "name": Tags.server_health,
            "description": "Verify server status and configuration variables.",
            "externalDocs": {
                "description": "Server Health Check",
                "url": "http://127.0.0.1:8000/docs#server_health",
            },
        },
    ]
