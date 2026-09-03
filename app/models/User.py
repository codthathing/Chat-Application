from __future__ import annotations
from re import match
from typing import TypedDict, TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from app.models.ChatRoom import DualChatRoom, MultiChatRoom, ChatRoom
    from app.models.Message import Message

class FriendEntry(TypedDict):
    username: str
    room: DualChatRoom

class GroupEntry(TypedDict):
    group_name: str
    room: MultiChatRoom

class User:
    from app.models.ChatRoom import DualChatRoom, MultiChatRoom

    users: list[User] = []

    def __init__(self, uid: str, username: str, email: str) -> None:
        if not match(r'^[a-zA-Z0-9_]+$', username):
            raise ValueError("Username can only contains a-Z, 0-9, _")
        
        if User.verify_username(username):
            raise ValueError("Username already exists")
        
        if User.verify_email(email):
            raise ValueError("Email used by a different user")

        self._id: str = uid
        self._username: str = username
        self._email: str = email
        self._friends: list[FriendEntry] = []
        self._groups: list[GroupEntry] = []

        User.users.append(self)

    @property
    def id(self) -> str:
        return self._id

    @property
    def username(self) -> str:
        return self._username
    
    @username.setter
    def username(self, new_username: str) -> None:
        # from app.models.ChatRoom import ChatRoom

        for u in ChatRoom.roomUsers:
            if u.user_id == self._id:
                u.username = new_username

        self._username = new_username
    
    @property 
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, new_email: str) -> None:
        from app.models.ChatRoom import ChatRoom

        for u in ChatRoom.roomUsers:
            if u.user_id == self._id:
                u.email = new_email
                
        self._email = new_email

    @property
    def friends(self) -> list[FriendEntry]:
        return self._friends

    @property
    def groups(self) -> list[GroupEntry]:
        return self._groups
    
    def __str__(self) -> str:
        return f"Username: {self.username}, Email={self.email}"
    
    def __repr__(self) -> str:
        return f"User(id={self._id}, username=@{self._username}, email={self._email})"
    
    @classmethod
    def verify_username(cls, username: str) -> bool:
        return bool(next((u for u in cls.users if u.username == username), None))
    
    @classmethod
    def verify_email(cls, email: str) -> bool:
        return bool(next((u for u in cls.users if u.email == email), None))
    
    def add_friends(self, username: str, room: DualChatRoom) -> None:
        self._friends.append({ "username": username, "room": room })

    def add_group(self, group_name: str, room: MultiChatRoom ) -> None:
        self._groups.append({ "group_name": group_name, "room": room })

    def update_username(self, new_username: str) -> str:
        if not match(r'^[a-zA-Z0-9_]+$', new_username):
            return "Username can only contain a-Z, 0-9, _"

        if User.verify_username(new_username):
            if self.username == new_username:
                return "Kindly enter a different username"
            else:
                return "Username already exists"
        else:
            self.username = new_username

            return "Username successfully changed!"

    def update_email(self, new_email: str) -> str:
        if User.verify_email(new_email):
            if self.email == new_email:
                return "Kindly enter a different email"
            else:
                return "Email already used by a different user"
        else:
            self.email = new_email

            return "Email successfully updated!"

    def create_dual_user_room(self, room_id: UUID, other_user: User) -> DualChatRoom:
        from app.models.ChatRoom import DualChatRoom

        return DualChatRoom(room_id, self, other_user)
    
    def create_multi_user_room(self, room_id: UUID, group_name: str, other_users: list[User] | None = None) -> MultiChatRoom:
        from app.models.ChatRoom import MultiChatRoom

        if not other_users:
            other_users = []

        return MultiChatRoom(room_id, group_name, self, other_users)
    


class MutualUser:
    def __init__(self, user_id: str, username: str, email: str) -> None:
        if not User.verify_username(username):
            raise ValueError("Not a user, create an account!")

        self._user_id: str = user_id
        self._username: str = username
        self._email: str = email
        self._messages: list[Message] = []

    @property
    def user_id(self) -> str:
        return self._user_id
    
    @property
    def username(self) -> str:
        return self._username
    
    @username.setter
    def username(self, new_username: str) -> None:
        self._username = new_username

    @property
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, new_email: str) -> None:
        self._email = new_email
    
    def __str__(self) -> str:
        return f"Username: {self._username}, Email={self._email})"
    
    def __repr__(self) -> str:
        return f"MutualUser(id={self._user_id}, username=@{self._username}, email={self._email}{", messages=" + str(self._messages) if bool(self._messages) else ''})"

    

class GroupUser(MutualUser):
    def __init__(self, user_id: str, username: str, email: str, room_status: str) -> None:
        super().__init__(user_id, username, email)
        self._room_status: str = room_status

    @property
    def room_status(self) -> str:
        return self._room_status

    @room_status.setter
    def room_status(self, new_room_status: str) -> None:
        self._room_status = new_room_status
    
    def __str__(self) -> str:
        return f"{super().__str__()}, Status: {self._room_status}"
    
    def __repr__(self) -> str:
        return f"GroupUser(id={self._user_id}, username=@{self._username}, email={self._email}, status={self._room_status}{", messages=" + str(self._messages) if bool(self._messages) else ''})"