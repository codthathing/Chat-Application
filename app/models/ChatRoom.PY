from abc import ABC, abstractmethod
from random import randint
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.User import User

class ChatRoom(ABC):
    chatrooms: list["ChatRoom"] = []

    def __init__(self, user: "User") -> None:
        if user.username not in user.__class__.usernames:
            raise ValueError("Not a user so can't create a room")

        self._room_id: int = randint(0, 1000)
        self._users: list[User] = [user]
        ChatRoom.chatrooms.append(self)

    @abstractmethod
    def __repr__(self) -> str:
        return f"id={self._room_id}, users={self._users}"




class DualUser(ChatRoom):
    def __init__(self, user: "User", other_user: "User") -> None:
        if other_user.username not in user.__class__.usernames:
            raise ValueError(f"{other_user.username} not a user, kindly create a room with a user")

        super().__init__(user)
        self._users.append(other_user)

    def __repr__(self) -> str:
        return f"DualUser({super().__repr__()})"




class MultiUser(ChatRoom):
    def __init__(self, user: "User", other_users: list["User"] = []) -> None:
        for u in other_users:
            if u.username not in user.__class__.usernames:
                raise ValueError(f"{user.username} not a user, kindly remove")


        super().__init__(user)
        self._admins: list[User] = [user]
        self._users.extend(other_users)

    def __repr__(self) -> str:
        return f"MultiUser({super().__repr__()}, admins={self._admins})"

    def addRoomAdmin(self, admin: "User", new_admin: "User") -> None:
        if admin not in self._admins:
            raise ValueError("Not a admin! can't add a new admin")
        
        if new_admin in self._admins:
            raise ValueError("User already a admin in group")
                
        self._admins.append(new_admin)

    def addUserToRoom(self, user: "User", new_user: "User") -> None:
        if user not in self._users:
            raise ValueError("Not a group member! Can't add a member")
        
        if new_user in self._users:
            raise ValueError("User already in group")

        self._users.append(new_user)