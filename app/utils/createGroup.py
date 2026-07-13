from typing import Callable, TypeVar
from models.ChatRoom import MultiChatRoom, ChatRoom
from models.User import User, GroupUser
from utils.types import UserDetailsFn

T = TypeVar("T")

def group_user_choices(user: User, userDetails: UserDetailsFn, choice, group_users: list[User] | None) -> list[User] | None:
    match choice:
        case 1:
            return create_group_options(user, userDetails, 1, group_users)
        case 2:
            return group_users
        case 3:
            userDetails(user)

            return None
        case _:
            choice = int(input(f"\nInvalid option {choice}, try again!\n\n1. Enter username\n2. Create group\n3. Cancel and Go home"))

            return group_user_choices(user, userDetails, choice, group_users)

def create_group_options(user: User, userDetails: UserDetailsFn, choice, group_users: list[User] | None = None) -> list[User] | None:
    if group_users is None:
        group_users = []

    match choice:
        case 1:
            new_user = input("\nEnter new username: ")

            new_group_user: User | None = next((u for u in User.users if u.username == new_user), None)

            if new_group_user:
                group_users.append(new_group_user)

                choice = int(input("\nUsername successfully added!!\n\n1. Enter another user\n2. Create group\n3. Cancel and Go home\n\n"))

                return group_user_choices(user, userDetails, choice, group_users)
            else:
                choice = int(input(f"\nUsername @{new_user} not a user!!\n\n1. Try again\n2. Create group\n3. Cancel and Go home\n\n"))

                return group_user_choices(user, userDetails, choice, group_users)
        case 2:
            return group_users
        case _:
            choice = int(input(f"\n{choice} not of the options available!\n\n1. Yes (Enter new users)\n2. No (Create group without users)\n\n"))

            return create_group_options(user, userDetails, choice, group_users)

def enter_chat(userDetails: UserDetailsFn, user: User, room: MultiChatRoom, group_name: str):
    message: str = input("\nNew message: ")

    room.enterChatToRoom(user.username, message)

    group_chat_details(userDetails, user, room, group_name)

def add_group_member_action(userDetails: UserDetailsFn, user: User, room: MultiChatRoom, group_name: str, username: str, action: Callable[[User, User], str], not_found_message: Callable[[str], str]) -> None:
    target_user: User | None = next((u for u in User.users if u.username == username), None)

    if target_user:
        result_string: str = action(user, target_user)

        print(result_string)
    else:
        print(not_found_message(username))

    group_chat_details(userDetails, user, room, group_name)

def add_user(userDetails: UserDetailsFn, user: User, room: MultiChatRoom, group_name: str):
    new_username: str = input("\nEnter new username: ")

    add_group_member_action(userDetails, user, room, group_name, new_username, room.addUserToRoom, lambda name: f"\n@{name} not a user, can't add to group!",)

def add_admin(userDetails: UserDetailsFn, user: User, room: MultiChatRoom, group_name: str):
    new_admin_username: str = input("\nEnter new admin username: ")

    add_group_member_action(userDetails, user, room, group_name, new_admin_username, room.addRoomAdmin, lambda name: f"\n@{name} not a user!",)

def user_view_group_options(choice: int, userDetails: UserDetailsFn, user: User, room: MultiChatRoom, group_name: str) -> None:
    match choice:
        case 1:
            enter_chat(userDetails, user, room, group_name)
        case 2:
            add_user(userDetails, user, room, group_name)
        case 4:
            userDetails(user)
        case _:
            choice = int(input(f"\n{choice} not part of options available!\n\n1. Enter chat to room\n2. Add a group member\n3. View group list\4. Go home\n\n"))

            user_view_group_options(choice, userDetails, user, room, group_name)

def user_view_group_admin_options(choice, userDetails: UserDetailsFn, user: User, room: MultiChatRoom, group_name: str) -> None:
    match choice:
        case 1:
            enter_chat(userDetails, user, room, group_name)
        case 2:
            add_admin(userDetails, user, room, group_name)
        case 3:
            add_user(userDetails, user, room, group_name)
        case 5:
            userDetails(user)
        case _:
            choice = int(input(f"\n{choice} not part of options available!\n\n. Enter chat to room\n2. Add admin from group members\n3. Add a group member\n4. View group list\n5. Go home\n\n"))

            user_view_group_admin_options(choice, userDetails, user, room, group_name)

def determine_user_group_options(userDetails: UserDetailsFn, user: User, room: MultiChatRoom, group_name: str) -> None:
    userGroupObject: GroupUser | None = next((u for u in room.users if u.username == user.username), None)

    if not userGroupObject:
        return

    if userGroupObject.room_status == "admin":
        choice = int(input("\n1. Enter chat to room\n2. Add admin from group members\n3. Add a group member\n4. View group list\n5. Go home\n\n"))

        user_view_group_admin_options(choice, userDetails, user, room, group_name)
    else:
        choice = int(input("\n1. Enter chat to room\n2. Add a group member\n3. View group list\4. Go home\n\n"))

        user_view_group_options(choice, userDetails, user, room, group_name)

def display_room_infos(title: str, items: list[T], sort_key: Callable[[T], object], formatter: Callable[[int, T], str]) -> None:
    if len(items) == 0:
        return

    print(f"\n{title}: ")

    sorted_items = sorted(items, key=sort_key)

    for i, item in enumerate(sorted_items):
        print(formatter(i, item))

def group_chat_details(userDetails: UserDetailsFn, user: User, room: MultiChatRoom, group_name: str):
    print(f"\nGroup Name: {group_name}")
    display_room_infos("Users", room.users, sort_key=lambda u: u.room_status != "admin",formatter=lambda i, u: f"{i + 1}: {u.username}{' (admin)' if u.room_status == 'admin' else ''}")
    display_room_infos("Messages", room.messages, sort_key=lambda m: m.created_at,formatter=lambda i, m: f"[{m.created_at}] {m.username}: {m.text}")

    determine_user_group_options(userDetails, user, room, group_name)

def group_created_options(choice, userDetails: UserDetailsFn, user: User, room: MultiChatRoom, group_name: str) -> None:
    match choice:
        case 1:
            group_chat_details(userDetails, user, room, group_name)
        case 3:
            userDetails(user)
        case _:
            choice = int(input(f"\n{choice} not part of options available\n\n1. Enter group chat\n2. View group list\n3. Go home\n\n"))

            group_created_options(choice, userDetails, user, room, group_name)

def create_group(user: User, userDetails: UserDetailsFn) -> None:
    group_name = input("\nEnter a group name: ")

    name_taken = any(isinstance(r, MultiChatRoom) and r.group_name == group_name for r in ChatRoom.chatrooms)

    if name_taken:
        choice = int(input("\nGroup chat name already taken!\n\n1. View group chat (authorised members only)\n2. View group list\n3. Create with a different group name\n4. Request to join group\n5. Go home\n\n"))
    else:
        choice = int(input("\nDo you want to enter new users? \n\n1. Yes (Enter new users)\n2. No (Create group as only user)\n\n"))

        group_users = create_group_options(user, userDetails, choice)

        if group_users is not None:
            multi_room = user.createMultiUserRoom(group_name, group_users)

            user.addGroup(group_name)

            choice = int(input("\nGroup successfully created!\n\n1. Enter group chat\n2. View group list\n3. Go home\n\n"))

            group_created_options(choice, userDetails, user, multi_room, group_name)