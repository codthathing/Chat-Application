from abc import ABC, abstractmethod
from random import randint
from typing import TYPE_CHECKING
from models.Message import Message

if TYPE_CHECKING:
    from models.User import User, GroupUser, MutualUser

class ChatRoom(ABC):
    chatrooms: list["DualChatRoom | MultiChatRoom"] = []
    roomUsers: list["GroupUser | MutualUser"] = []

    def __init__(self, user: "User") -> None:
        from models.User import User

        if user not in User.users:
            raise ValueError("Not a user so can't create a room")

        self._room_id: int = randint(0, 1000)
    
    @property
    def room_id(self) -> int:
        return self._room_id

    @abstractmethod
    def __repr__(self) -> str:
        return f"id={self._room_id}, users="



class DualChatRoom(ChatRoom):
    def __init__(self, user: "User", other_user: "User") -> None:
        from models.User import User, MutualUser

        if other_user not in User.users:
            raise ValueError(f"{other_user.username} not a user, kindly create a room with a user")

        super().__init__(user)
        self._users: list[MutualUser] = []
        self._users.extend(MutualUser(u.id, u.username, u.email) for u in [user, other_user])
        self._messages: list[Message] = []
        ChatRoom.roomUsers.extend(self._users)
        ChatRoom.chatrooms.append(self)

    @property
    def users(self) -> list["MutualUser"]:
        return self._users
    
    @property
    def messages(self) -> list[Message]:
        return self._messages

    def __repr__(self) -> str:
        return f"DualChatRoom({super().__repr__()}{self._users})"
    
    def enterChatToRoom(self, username: str, text: str) -> None:
        userObject: MutualUser | None = next((u for u in self._users if u.username == username), None)

        if not userObject:
            raise ValueError("Not a member of this chat! can't enter message to chat")
        
        self._messages.append(Message(username, text))



class MultiChatRoom(ChatRoom):
    def __init__(self, user: "User", other_users: list["User"] = []) -> None:
        from models.User import User, GroupUser

        for u in other_users:
            if u not in User.users:
                raise ValueError(f"{user.username} not a user, kindly remove")

        super().__init__(user)
        self._users: list[GroupUser] = []
        self._users.append(GroupUser(user.id, user.username, user.email, "admin"))
        self._users.extend(map(lambda u: GroupUser(u.id, u.username, u.email, "user") , other_users))
        self._messages: list[Message] = []
        ChatRoom.roomUsers.extend(self._users)
        ChatRoom.chatrooms.append(self)

    @property
    def users(self) -> list["GroupUser"]:
        return self._users
    
    @property
    def messages(self) -> list[Message]:
        return self._messages

    def __repr__(self) -> str:
        return f"MultiChatRoom({super().__repr__()}{self._users})"

    def addRoomAdmin(self, admin: "User", new_admin: "User") -> str:
        adminObject: GroupUser | None = next((u for u in self._users if u.username == admin.username), None)
        newAdminObject: GroupUser | None = next((u for u in self._users if u.username == new_admin.username), None)

        if not adminObject:
            return "\nNot in group! kindly request to join"
        
        if not newAdminObject:
            return f"\n{new_admin.username} not in group! kindly add"

        if adminObject.room_status != "admin":
            return "\nNot a admin! can't add a new admin"
        
        if newAdminObject.room_status == "admin":
            return "\nUser already a admin in group"
                
        newAdminObject.room_status = "admin"

        return "\nNew admin successfully added to the group!"

    def addUserToRoom(self, user: "User", new_user: "User") -> str:
        from models.User import GroupUser

        userObject: GroupUser | None = next((u for u in self._users if u.username == user.username), None)
        newUserObject: GroupUser | None = next((u for u in self._users if u.username == new_user.username), None)

        if not userObject:
            return "\nNot a group member! kindly request to join"
        
        if newUserObject:
            return "\nNew user already in group"

        newUser = GroupUser(new_user.id, new_user.username, new_user.email, "user")
        self._users.append(newUser)
        ChatRoom.roomUsers.append(newUser)

        return "\nNew user successfully added to the group!"

    def enterChatToRoom(self, username: str, text: str) -> str | None:
        userObject: GroupUser | None = next((u for u in self._users if u.username == username), None)

        if not userObject:
            return "Not a member of this group! can't enter message to the group"
        
        self._messages.append(Message(username, text))

        return None