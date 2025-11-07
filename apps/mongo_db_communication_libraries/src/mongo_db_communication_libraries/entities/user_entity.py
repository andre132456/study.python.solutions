from beanie import Document


class User(Document):
    """A simple User entity."""

    name: str
    email: str

    class Settings:
        name = "users"
