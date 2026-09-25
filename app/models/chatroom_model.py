from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from typing import TYPE_CHECKING
from app.models.message_model import Message

if TYPE_CHECKING:
    from app.models.user_model import User, GroupUser, MutualUser

class ChatRoom(ABC):
    chatroom: list[DualChatRoom | MultiChatRoom] = []
    roomUsers: list[MutualUser | GroupUser] = []

    def __init__(self, room_id: UUID) -> None:
        self._id: UUID = room_id
        self._messages: list[Message] | None = None
    
    @property
    def room_id(self) -> UUID:
        return self._id

    @property
    def messages(self) -> list[Message] | None:
        if self._messages is None:
            return None
        return self._messages

    @messages.setter
    def messages(self, messages: list[Message]) -> None:
        self._messages: list[Message] = messages

    @abstractmethod
    def enter_chat_to_room(self, username: str, text: str, time_stamp: str) -> None:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        return f"id={self._id}, users="



class DualChatRoom(ChatRoom):
    def __init__(self, room_id: UUID, user: User, other_user: User) -> None:
        from app.models.user_model import MutualUser

        super().__init__(room_id)
        self._users: list[MutualUser] = [MutualUser(u.id, u.username, u.email) for u in [user, other_user]]

        ChatRoom.chatroom.append(self)
        ChatRoom.roomUsers.extend(self._users)

    @property
    def users(self) -> list[MutualUser]:
        return self._users

    def enter_chat_to_room(self, username: str, text: str, time_stamp: str) -> str | None:
        user_object: MutualUser | None = next((u for u in self._users if u.username == username), None)

        if not user_object:
            return "\nNot a member of this chat! can't enter message to chat"

        if self._messages is not None:
            self._messages.append(Message(username, text, time_stamp))

        return None

    def __repr__(self) -> str:
        return f"DualChatRoom({super().__repr__()}{self._users})"



class MultiChatRoom(ChatRoom):
    def __init__(self, room_id: UUID, group_name: str, user: User | None = None, other_users: list[User] | None = None) -> None:
        from app.models.user_model import GroupUser

        super().__init__(room_id)
        self._group_name: str = group_name
        self._users: list[GroupUser] | None = None

        if user and self._users:
            self._users.append(GroupUser(user.id, user.username, user.email, "admin"))

        if other_users and self._users:
            self._users.extend(map(lambda other_u: GroupUser(other_u.id, other_u.username, other_u.email, "member") , other_users))

        ChatRoom.chatroom.append(self)
        if self._users:
            ChatRoom.roomUsers.extend(self._users)

    @property
    def group_name(self) -> str:
        return self._group_name

    @property
    def users(self) -> list[GroupUser] | None:
        if self._users is None:
            return None

        return self._users

    @users.setter
    def users(self, users: list[GroupUser]) -> None:
        self._users: list[GroupUser] = users

    def add_room_admin(self, admin: User, new_admin: User) -> str:
        if self._users is None:
            return "\nNo user in group! Can't add new admin"

        admin_object: GroupUser | None = next((u for u in self._users if u.username == admin.username), None)
        new_admin_object: GroupUser | None = next((u for u in self._users if u.username == new_admin.username), None)

        if not admin_object:
            return "\nNot in group! kindly request to join"
        
        if not new_admin_object:
            return f"\n{new_admin.username} not in group! kindly add"

        if admin_object.role != "admin":
            return "\nNot a admin! can't add a new admin"
        
        if new_admin_object.role == "admin":
            return "\nUser already a admin in group"
                
        new_admin_object.role = "admin"

        return "success"

    def add_user_to_room(self, user: User, new_user: User) -> str:
        if self._users is None:
            return "\nNo user in group! Can't add new user"

        from app.models.user_model import GroupUser

        user_object: GroupUser | None = next((u for u in self._users if u.username == user.username), None)
        new_user_object: GroupUser | None = next((u for u in self._users if u.username == new_user.username), None)

        if not user_object:
            return "\nNot a group member! kindly request to join"

        if new_user_object:
            return "\nNew user already in group"

        new_user = GroupUser(new_user.id, new_user.username, new_user.email, "member")
        self._users.append(new_user)

        return "success"

    def enter_chat_to_room(self, username: str, text: str, time_stamp: str) -> str | None:
        if self._users is None:
            return "\nNo user in group! Can't enter message to chat"

        user_object: GroupUser | None = next((u for u in self._users if u.username == username), None)

        if not user_object:
            return "\nNot a member of this group! can't enter message to the group"

        if self._messages is not None:
            self._messages.append(Message(username, text, time_stamp))

        return None

    def __repr__(self) -> str:
        return f"MultiChatRoom({super().__repr__()}{self._users})"