from aiogram.types import CallbackQuery
from aiogram.types import Message


class UserDataResolver:
    def __init__(self, obj):
        """
        Initialize with either a Message or CallbackQuery object.
        :param obj: Message or CallbackQuery instance
        """
        if isinstance(obj, (Message, CallbackQuery)):
            self._user = obj.from_user
        else:
            msg = f"Expected Message or CallbackQuery, got {type(obj).__name__}"
            raise TypeError(msg)

    @property
    def id(self):
        return self._user.id

    @property
    def username(self):
        return self._user.username

    @property
    def first_name(self):
        return self._user.first_name

    @property
    def last_name(self):
        # Provide a default if last_name is None
        return self._user.last_name or "not_available"

    def to_dict(self):
        """Convert the user data to a dictionary."""
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }

    def __str__(self):
        """Readable string representation of the user data."""
        return (
            f"User(ID: {self.id}, Username: {self.username}, "
            f"First Name: {self.first_name}, Last Name: {self.last_name})"
        )
