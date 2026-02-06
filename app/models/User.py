from models.Message import Message
from models.ChatRoom import DualUser, MultiUser
from time import localtime, strftime

class User:
    users: list["User"] = []

    def __init__(self, username: str, email: str) -> None:
        if username.isalnum():
            raise ValueError("Username must contain at least one non-alphanumeric character")
        
        if User.verifyUsername(username):
            raise ValueError("Username already exists")

        self._username: str = username
        self._email: str = email

        User.users.append(self)

    @property
    def username(self) -> str:
        return self._username
    
    @property 
    def email(self) -> str:
        return self._email
    
    def __str__(self) -> str:
        return f"Username: {self.username}, Email={self.email}"
    
    def __repr__(self) -> str:
        return f"User(username={self._username}, email={self._email})"
    
    @classmethod
    def verifyUsername(cls, username: str) -> bool:
        return bool(next((u for u in cls.users if u.username == username), None))

    def createDualUserRoom(self, other_user: "User") -> DualUser:
        return DualUser(self, other_user)
    
    def createMultiUserRoom(self, other_users: list["User"] = []) -> MultiUser:
        return MultiUser(self, other_users)
    


class MutualUser:
    def __init__(self, username: str, email: str) -> None:
        if not User.verifyUsername(username):
            raise ValueError("Not a user, create an account!")

        self._username: str = username
        self._email: str = email
        self._messages: list[Message] = []

    @property
    def username(self) -> str:
        return self._username

    @property
    def email(self) -> str:
        return self._email
    
    def __str__(self) -> str:
        return f"Username: {self._username}, Email={self._email})"
    
    def __repr__(self) -> str:
        return f"MutualUser(username={self._username}, email={self._email}{", messages=" + str(self._messages) if bool(self._messages) else ''})"
    
    def createChat(self, message: str) -> None:
        self._messages.append(Message(strftime("%H:%M:%S", localtime()), message))

    

class GroupUser(MutualUser):
    def __init__(self, username: str, email: str, room_status: str) -> None:
        super().__init__(username, email)
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
        return f"GroupUser(username={self._username}, email={self._email}, status={self._room_status}{", messages=" + str(self._messages) if bool(self._messages) else ''})"