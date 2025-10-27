from typing import List, Optional
import logging

from .schemas import KeysCreate, KeysRead, KeysUpdate
from .repository import KeysRepository
from .helpers import generate_secret_key

logger = logging.getLogger(__name__)


class KeysService:
    """
    Business logic layer for secret key management.

    This service handles operations related to secret keys including
    CRUD operations and key-to-strategy-name lookups.
    """
    def __init__(self, repo: KeysRepository):
        self.repo = repo

    async def list(self) -> List[KeysRead]:
        """List all secret keys."""
        return await self.repo.list()

    async def get(self, item_id: str) -> Optional[KeysRead]:
        """Get a secret key entry by ID."""
        return await self.repo.get(item_id)

    async def create(self, payload: KeysCreate) -> KeysRead:
        """
        Create a new secret key entry.

        Args:
            payload: Key creation data

        Returns:
            The created key entry
        """
        # If no secret_key provided, generate one
        if not payload.secret_key:
            payload.secret_key = generate_secret_key()
            logger.info(f"Generated new secret key for strategy: {payload.name}")

        return await self.repo.create(payload)

    async def update(self, item_id: str, payload: KeysUpdate) -> Optional[KeysRead]:
        """Update an existing secret key entry."""
        return await self.repo.update(item_id, payload)

    async def delete(self, item_id: str) -> bool:
        """Delete a secret key entry."""
        return await self.repo.delete(item_id)

    async def get_name_by_key(self, secret_key: str) -> Optional[str]:
        """
        Look up a strategy name by its secret key.

        This is an optimized query using an indexed field for fast lookups.

        Args:
            secret_key: The secret key to search for

        Returns:
            The strategy name if found, None otherwise
        """
        key_entry = await self.repo.get_by_secret_key(secret_key)
        if key_entry:
            logger.debug(f"Found strategy name for key: {key_entry.name}")
            return key_entry.name
        logger.warning(f"No strategy found for provided secret key")
        return None


async def get_service() -> KeysService:
    """Dependency injection for KeysService."""
    repo = KeysRepository()
    return KeysService(repo)
