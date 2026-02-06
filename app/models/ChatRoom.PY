from abc import ABC, abstractmethod
from random import randint
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.User import User, GroupUser, MutualUser

class ChatRoom(ABC):
    chatrooms: list["ChatRoom"] = []

    def __init__(self, user: "User") -> None:
        from models.User import User

        if user not in User.users:
            raise ValueError("Not a user so can't create a room")

        self._room_id: int = randint(0, 1000)
        ChatRoom.chatrooms.append(self)

    @abstractmethod
    def __repr__(self) -> str:
        return f"id={self._room_id}, users="



class DualUser(ChatRoom):
    def __init__(self, user: "User", other_user: "User") -> None:
        from models.User import User, MutualUser

        if other_user not in User.users:
            raise ValueError(f"{other_user.username} not a user, kindly create a room with a user")

        super().__init__(user)
        self._users: list[MutualUser] = []
        self._users.extend(MutualUser(u.username, u.email) for u in [user, other_user])

    def __repr__(self) -> str:
        return f"DualUser({super().__repr__()}{self._users})"
    
    def enterChatToRoom(self, user: "User", text: str) -> None:
        userObject: MutualUser | None = next((u for u in self._users if u.username == user.username), None)

        if not userObject:
            raise ValueError("Not a user! can't enter message to room")
        
        userObject.createChat(text)



class MultiUser(ChatRoom):
    def __init__(self, user: "User", other_users: list["User"] = []) -> None:
        from models.User import User, GroupUser

        for u in other_users:
            if u not in User.users:
                raise ValueError(f"{user.username} not a user, kindly remove")

        super().__init__(user)
        self._users: list[GroupUser] = []
        self._users.append(GroupUser(user.username, user.email, "admin"))
        self._users.extend(map(lambda u: GroupUser(u.username, u.email, "user") , other_users))

    def __repr__(self) -> str:
        return f"MultiUser({super().__repr__()}{self._users})"

    def addRoomAdmin(self, admin: "User", new_admin: "User") -> None:
        adminObject: GroupUser | None = next((u for u in self._users if u.username == admin.username), None)
        newAdminObject: GroupUser | None = next((u for u in self._users if u.username == new_admin.username), None)

        if not adminObject:
            raise ValueError("Not in group! kindly request to join")
        
        if not newAdminObject:
            raise ValueError(f"{new_admin.username} not in group! kindly add")

        if adminObject.room_status != "admin":
            raise ValueError("Not a admin! can't add a new admin")
        
        if newAdminObject.room_status == "admin":
            raise ValueError("User already a admin in group")
                
        newAdminObject.room_status = "admin"

    def addUserToRoom(self, user: "User", new_user: "User") -> None:
        from models.User import GroupUser

        userObject: GroupUser | None = next((u for u in self._users if u.username == user.username), None)
        newUserObject: GroupUser | None = next((u for u in self._users if u.username == new_user.username), None)

        if not userObject:
            raise ValueError("Not a group member! kindly request to join")
        
        if newUserObject:
            raise ValueError("User already in group")

        self._users.append(GroupUser(new_user.username, new_user.email, "user"))

    def enterChatToRoom(self, user: "User", text: str) -> None:
        userObject: GroupUser | None = next((u for u in self._users if u.username == user.username), None)

        if not userObject:
            raise ValueError("Not a user! can't enter message to room")
        
        userObject.createChat(text)