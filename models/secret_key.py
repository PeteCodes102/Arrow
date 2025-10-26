from beanie import Document
from typing import Optional


class SecretKeyIndex(Document):
    secret_key: str
    name: str
    description: Optional[str] = None

    class Settings:
        name = "secret_key_index"
