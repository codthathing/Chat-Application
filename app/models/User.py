from models.Message import Message
from models.ChatRoom import DualChatRoom, MultiChatRoom, ChatRoom
from random import randint
from re import match
from typing import TypedDict

class FriendEntry(TypedDict):
    username: str
    room: DualChatRoom

class User:
    users: list["User"] = []

    def __init__(self, username: str, email: str) -> None:
        if not match(r'^[a-zA-Z0-9_]+$', username):
            raise ValueError("Username can only conta a-Z, 0-9, _")
        
        if User.verifyUsername(username):
            raise ValueError("Username already exists")
        
        if User.verifyEmail(email):
            raise ValueError("Email used by a different user")

        self._id: int = randint(0, 1000)
        self._username: str = username
        self._email: str = email
        self._friends: list[FriendEntry] = []
        self._groups: list[str] = []

        User.users.append(self)

    @property
    def id(self) -> int:
        return self._id

    @property
    def username(self) -> str:
        return self._username
    
    @username.setter
    def username(self, new_username: str) -> None:
        for u in ChatRoom.roomUsers:
            if u.id == self._id:
                u.username = new_username

        self._username = new_username
    
    @property 
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, new_email: str) -> None:
        for u in ChatRoom.roomUsers:
            if u.id == self._id:
                u.email = new_email
                
        self._email = new_email

    @property
    def friends(self) -> list[FriendEntry]:
        return self._friends

    @property
    def groups(self) -> list[str]:
        return self._groups
    
    def __str__(self) -> str:
        return f"Username: {self.username}, Email={self.email}"
    
    def __repr__(self) -> str:
        return f"User(id={self._id}, username=@{self._username}, email={self._email})"
    
    @classmethod
    def verifyUsername(cls, username: str) -> bool:
        return bool(next((u for u in cls.users if u.username == username), None))
    
    @classmethod
    def verifyEmail(cls, email: str) -> bool:
        return bool(next((u for u in cls.users if u.email == email), None))
    
    def addFriends(self, username: str, room: DualChatRoom) -> None:
        self._friends.append({ "username": username, "room": room })

    def addGroup(self, group_name: str) -> None:
        self._groups.append(group_name)

    def updateUsername(self, new_username: str) -> None:
        if not match(r'^[a-zA-Z0-9_]+$', new_username):
            raise ValueError("Username can only conta a-Z, 0-9, _")
        
        if User.verifyUsername(new_username):
            if self.username == new_username:
                raise ValueError("Kindly enter a different username")
            else:
                raise ValueError("Username already exists")
        else:
            self.username = new_username

    def updateEmail(self, new_email: str) -> None:
        if User.verifyEmail(new_email):
            if self.email == new_email:
                raise ValueError("Kindly enter a different email")
            else:
                raise ValueError("Email already used by a different user")
        else:
            self.email = new_email

    def createDualUserRoom(self, other_user: "User") -> DualChatRoom:
        return DualChatRoom(self, other_user)
    
    def createMultiUserRoom(self, group_name: str, other_users: list["User"] = []) -> MultiChatRoom:
        return MultiChatRoom(group_name, self, other_users)
    


class MutualUser:
    def __init__(self, id: int, username: str, email: str) -> None:
        if not User.verifyUsername(username):
            raise ValueError("Not a user, create an account!")

        self._id: int = id
        self._username: str = username
        self._email: str = email
        self._messages: list[Message] = []

    @property
    def id(self) -> int:
        return self._id
    
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
        return f"MutualUser(id={self._id}, username=@{self._username}, email={self._email}{", messages=" + str(self._messages) if bool(self._messages) else ''})"

    

class GroupUser(MutualUser):
    def __init__(self, id: int, username: str, email: str, room_status: str) -> None:
        super().__init__(id, username, email)
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
        return f"GroupUser(id={self._id}, username=@{self._username}, email={self._email}, status={self._room_status}{", messages=" + str(self._messages) if bool(self._messages) else ''})"