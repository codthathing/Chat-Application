from app.models.chatroom_model import MultiChatRoom, ChatRoom
from requests import get
from app.models.user_model import GroupUser

def get_room_users(room: MultiChatRoom):
    if room.users is None:
        response = get(f"http://127.0.0.1:8000/group-members/{room.room_id}")

        if not response.ok:
            print("\nUnable to get room members")
        else:
            data = response.json()

            users: list[GroupUser] = []

            for user in data:
                users.append(GroupUser(user["id"], user["username"], user["email"], user["role"]))

            ChatRoom.roomUsers.extend(users)
            room.users = users