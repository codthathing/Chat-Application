from app.utils.display_room_infos import display_room_infos
from app.checkers.types import UserDetailsFn, FriendsListFn
from app.models.chatroom_model import DualChatRoom
from app.models.user_model import User

def display_mutual_messages(user: User, user_details: UserDetailsFn, friends_list: FriendsListFn, room: DualChatRoom):
    from app.services.add_friend_service import friend_chat_options

    room_messages = room.messages

    if room_messages is not None:
        if len(room_messages) > 0:
            print("")

        display_room_infos(room_messages, sort_key=lambda m: m.created_at, formatter=lambda i, m: f"[{m.created_at}] {m.username}: {m.text}")

    choice = int(input("\n1. Enter new chat\n2. View friend list\n3. Go home\n\n"))

    friend_chat_options(user_details, friends_list, choice, user, room)