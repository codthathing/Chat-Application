from app.models.User import User
from app.models.ChatRoom import ChatRoom

class UsersRoomSchema():
    def __repr__(self) -> str:
        return f"""
Users: {User.users}\n
Rooms: {ChatRoom.chatrooms}
"""

