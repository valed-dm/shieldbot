from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup

if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext


class UsernameInputState(StatesGroup):
    entering_username = State()


class FSMStateManager:
    def __init__(self, state: FSMContext):
        """
        Initialize the FSMStateManager with the given FSMContext.
        """
        self._state = state
        self._data = {}

    async def load(self) -> None:
        """
        Load the current FSM state data into the manager.
        """
        self._data = await self._state.get_data()

    async def save(self) -> None:
        """
        Save the current state data back to the FSM context.
        """
        await self._state.set_data(self._data)

    def __getattr__(self, key: str) -> Any | None:
        """
        Access a state key as a property.
        """
        return self._data.get(key)

    def __setattr__(self, key: str, value: Any) -> None:
        """
        Set a state key as a property.
        """
        if key in ("_state", "_data"):
            super().__setattr__(key, value)
        else:
            self._data[key] = value

    def __delattr__(self, key: str) -> None:
        """
        Delete a state key as a property.
        """
        if key in self._data:
            del self._data[key]

    async def clear(self) -> None:
        """
        Clear all data from the FSM state.
        """
        self._data.clear()
        await self._state.clear()
