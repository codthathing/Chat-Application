from models.User import User
from models.ChatRoom import ChatRoom

class UsersRoomSchema():
    def __repr__(self) -> str:
        return f"""
Users: {User.users}\n
Rooms: {ChatRoom.chatrooms}
"""
    def createUser(self, username: str, email: str) -> User:
        return User(username, email)
    
    def updateUsername(self, user: User, new_username: str):
        if new_username.isalnum():
            raise ValueError("Username must not be alphanumeric")
        
        if User.verifyUsername(new_username):
            if self._username == new_username:
                raise ValueError("Kindly enter a different username")
            else:
                raise ValueError("Username already exists")

        self._username = new_username

    def updateEmail(self):
        pass

    def deleteUser(self):
        pass

