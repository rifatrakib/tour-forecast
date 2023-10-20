from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict
from pydash import camel_case


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=camel_case,
        json_encoders={
            datetime: lambda v: v.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z"),
        },
    )
