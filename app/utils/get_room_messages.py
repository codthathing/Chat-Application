from app.models.chatroom_model import ChatRoom
from app.models.message_model import Message
from requests import get

def get_room_messages(room: ChatRoom):
    if room.messages is None:
        response = get(f"http://127.0.0.1:8000/messages/{room.room_id}")

        if not response.ok:
            print("\nUnable to fetch room messages!")
        else:
            data = response.json()

            messages: list[Message] = []

            for m in data:
                messages.append(Message(m["username"], m["text"], m["time_stamp"]))

            room.messages = messages