import json
from uuid import UUID


class UUIDEncoder(json.JSONEncoder):
    def default(self: "UUIDEncoder", obj: object) -> str:
        if isinstance(obj, UUID):
            return str(obj)
        return super().default(obj)
