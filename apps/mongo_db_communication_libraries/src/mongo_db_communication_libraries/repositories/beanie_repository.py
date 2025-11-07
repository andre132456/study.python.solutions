from typing import Optional

import motor.motor_asyncio
from beanie import PydanticObjectId, init_beanie
from mongo_db_communication_libraries.entities.user_entity import User


class BeanieRepository:
    def __init__(
        self,
        connection_string: str = "mongodb://localhost:27017",
        database_name: str = "test_db",
    ):
        """Initialize the repository with connection details."""
        self.connection_string = connection_string
        self.database_name = database_name
        self.client: Optional[motor.motor_asyncio.AsyncIOMotorClient] = None
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize the database connection and Beanie."""
        if not self._initialized:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(self.connection_string)
            await init_beanie(
                database=self.client[self.database_name], document_models=[User]
            )
            self._initialized = True

    async def close(self) -> None:
        """Close the database connection."""
        if self.client:
            self.client.close()
            self._initialized = False

    async def create_user(self, name: str, email: str, session=None) -> User:
        """Create a new user in the database."""
        user = User(name=name, email=email)
        await user.insert(session=session)
        return user

    async def get_user_by_id(
        self, user_id: PydanticObjectId, session=None
    ) -> Optional[User]:
        """Retrieve a user by their ID."""
        return await User.get(user_id, session=session)

    async def get_all_users(self) -> list[User]:
        """Retrieve all users from the database."""
        return await User.find_all().to_list()

    async def update_user(
        self,
        user_id: PydanticObjectId,
        name: Optional[str] = None,
        email: Optional[str] = None,
    ) -> Optional[User]:
        """Update a user's information."""
        user = await User.get(user_id)
        if user:
            if name is not None:
                user.name = name
            if email is not None:
                user.email = email
            await user.save()
        return user

    async def delete_user(self, user_id: PydanticObjectId) -> bool:
        """Delete a user by their ID."""
        user = await User.get(user_id)
        if user:
            await user.delete()
            return True
        return False
