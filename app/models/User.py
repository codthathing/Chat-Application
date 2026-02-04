from models.Message import Message
from models.ChatRoom import ChatRoom, DualUser, MultiUser
from typing import Union, cast

class User:
    usernames: list[str] = []

    def __init__(self, username: str, email: str = "", password: str = "") -> None:
        if username.isalnum():
            raise ValueError("Username must contain at least one non-alphanumeric character")
        
        if User.verifyUsername(username):
            raise ValueError("Username already exists")

        self._username: str = username
        self._email: str = email
        self._password: str = password
        self._messages: list[Message] = []

        User.usernames.append(username)

    @property
    def username(self) -> str:
        return self._username
    
    @property 
    def email(self) -> str:
        return self._email
    
    @username.setter
    def username(self, new_username: str) -> None:
        if new_username.isalnum():
            raise ValueError("Username must not be alphanumeric")
        
        if User.verifyUsername(new_username):
            if self._username == new_username:
                raise ValueError("Kindly enter a different username")
            else:
                raise ValueError("Username already exists")
        
        User.usernames.remove(self._username)

        self._username = new_username
        User.usernames.append(new_username)
    
    def __repr__(self) -> str:
        return f"User(username={self.username}, email={self.email})"
    
    @classmethod
    def verifyUsername(cls, username: str) -> bool:
        return username in cls.usernames
    
    def inputChat(self, message: Message) -> None:
        self._messages.append(message)

    def createChatRoom(self, type: str, other_user: Union["User", list["User"], str] = "") -> Union[DualUser, MultiUser]:
        chat: ChatRoom

        if type == "dual" and not isinstance(other_user, User):
            raise ValueError("A single user is required with dual")
        
        if type == "multi" and not isinstance(other_user, list):
            raise ValueError("A list of users is required with multi")

        if type == "dual":
            chat = DualUser(self, cast(User, other_user))
        else:
            chat = MultiUser(self, cast(list[User] , other_user))

        return chat