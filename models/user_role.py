from enum import (
    Enum,
    auto,
)


class UserRole(Enum):
    normal = auto()
    guest = auto()
    admin = auto()