from beanie import Document, Indexed
from typing import Optional


class SecretKeyIndex(Document):
    """
    MongoDB document model for storing secret keys and their associated strategy names.

    This model maintains the mapping between cryptographically secure secret keys
    and strategy names, enabling authenticated alert creation.

    Fields:
        secret_key: Unique cryptographic key for authentication
        name: Strategy name associated with this key
        description: Optional description of the key's purpose
    """
    secret_key: Indexed(str, unique=True)  # Unique index for fast lookups
    name: Indexed(str)  # Index for searching by strategy name
    description: Optional[str] = None

    class Settings:
        name = "secret_key_index"
