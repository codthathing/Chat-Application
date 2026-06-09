from models.User import User
from models.ChatRoom import ChatRoom
from re import match

class UsersRoomSchema():
    def __repr__(self) -> str:
        return f"""
Users: {User.users}\n
Rooms: {ChatRoom.chatrooms}
"""
    def createUser(self, username: str, email: str) -> User:
        return User(username, email)
    
    def updateUsername(self, user: User, new_username: str) -> None:
        if not match(r'^[a-zA-Z0-9_]+$', new_username):
            raise ValueError("Username can only conta a-Z, 0-9, _")
        
        if User.verifyUsername(new_username):
            if user.username == new_username:
                raise ValueError("Kindly enter a different username")
            else:
                raise ValueError("Username already exists")
        else:
            user.username = new_username

    def updateEmail(self, user: User, new_email: str) -> None:
        if User.verifyEmail(new_email):
            if user.email == new_email:
                raise ValueError("Kindly enter a different email")
            else:
                raise ValueError("Email already used by a different user")
        else:
            user.email = new_email

