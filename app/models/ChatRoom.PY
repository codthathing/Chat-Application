from abc import ABC, abstractmethod
from random import randint
from typing import TYPE_CHECKING
from models.Message import Message

if TYPE_CHECKING:
    from models.User import User, GroupUser, MutualUser

class ChatRoom(ABC):
    chatroom: list["DualChatRoom | MultiChatRoom"] = []
    roomUsers: list["MutualUser | GroupUser"] = []

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
        ChatRoom.chatroom.append(self)
        ChatRoom.roomUsers.extend(self._users)

    @property
    def users(self) -> list["MutualUser"]:
        return self._users
    
    @property
    def messages(self) -> list[Message]:
        return self._messages

    def __repr__(self) -> str:
        return f"DualChatRoom({super().__repr__()}{self._users})"
    
    def enter_chat_to_room(self, username: str, text: str) -> None:
        user_object: MutualUser | None = next((u for u in self._users if u.username == username), None)

        if not user_object:
            raise ValueError("Not a member of this chat! can't enter message to chat")
        
        self._messages.append(Message(username, text))



class MultiChatRoom(ChatRoom):
    def __init__(self, group_name: str, user: "User", other_users: list["User"] | None = None) -> None:
        if not other_users:
            other_users = []

        from models.User import User, GroupUser

        for u in other_users:
            if u not in User.users:
                raise ValueError(f"{user.username} not a user, kindly remove")

        super().__init__(user)
        self._group_name: str = group_name
        self._users: list[GroupUser] = []
        self._users.append(GroupUser(user.id, user.username, user.email, "admin"))
        self._users.extend(map(lambda other_u: GroupUser(other_u.id, other_u.username, other_u.email, "user") , other_users))
        self._messages: list[Message] = []
        ChatRoom.chatroom.append(self)
        ChatRoom.roomUsers.extend(self._users)

    @property
    def group_name(self) -> str:
        return self._group_name

    @property
    def users(self) -> list["GroupUser"]:
        return self._users
    
    @property
    def messages(self) -> list[Message]:
        return self._messages

    def __repr__(self) -> str:
        return f"MultiChatRoom({super().__repr__()}{self._users})"

    def add_room_admin(self, admin: "User", new_admin: "User") -> str:
        admin_object: GroupUser | None = next((u for u in self._users if u.username == admin.username), None)
        new_admin_object: GroupUser | None = next((u for u in self._users if u.username == new_admin.username), None)

        if not admin_object:
            return "\nNot in group! kindly request to join"
        
        if not new_admin_object:
            return f"\n{new_admin.username} not in group! kindly add"

        if admin_object.room_status != "admin":
            return "\nNot a admin! can't add a new admin"
        
        if new_admin_object.room_status == "admin":
            return "\nUser already a admin in group"
                
        new_admin_object.room_status = "admin"

        return "\nNew admin successfully added to the group!"

    def add_user_to_room(self, user: "User", new_user: "User") -> str:
        from models.User import GroupUser

        user_object: GroupUser | None = next((u for u in self._users if u.username == user.username), None)
        new_user_object: GroupUser | None = next((u for u in self._users if u.username == new_user.username), None)

        if not user_object:
            return "\nNot a group member! kindly request to join"
        
        if new_user_object:
            return "\nNew user already in group"

        new_user = GroupUser(new_user.id, new_user.username, new_user.email, "user")
        self._users.append(new_user)
        ChatRoom.roomUsers.append(new_user)

        return "\nNew user successfully added to the group!"

    def enter_chat_to_room(self, username: str, text: str) -> str | None:
        user_object: GroupUser | None = next((u for u in self._users if u.username == username), None)

        if not user_object:
            return "Not a member of this group! can't enter message to the group"
        
        self._messages.append(Message(username, text))

        return None