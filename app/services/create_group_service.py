from typing import Callable, TypeVar
from app.models.chatroom_model import MultiChatRoom
from app.models.user_model import User, GroupUser
from app.checkers.types import UserDetailsFn, GroupsListFn, FriendAddConditionFn, FriendsListFn
from requests import post, Response, patch

from app.utils.get_room_messages import get_room_messages
from app.utils.get_room_users import get_room_users
from app.utils.display_room_infos import display_room_infos

T = TypeVar("T")

def group_user_choices(user: User, user_details: UserDetailsFn, friend_add_condition: FriendAddConditionFn, friends_list: FriendsListFn, choice, group_users: list[User] | None) -> list[User] | None:
    match choice:
        case 1:
            return create_group_options(user, user_details, 1, friend_add_condition, friends_list, group_users)
        case 2:
            return group_users
        case 3:
            user_details(user)

            return None
        case _:
            choice = int(input(f"\nInvalid option {choice}, try again!\n\n1. Enter username\n2. Create group\n3. Cancel and Go home"))

            return group_user_choices(user, user_details, friend_add_condition, friends_list, choice, group_users)

def no_group_user_choices(user: User, user_details: UserDetailsFn, friend_add_condition: FriendAddConditionFn, friends_list: FriendsListFn, choice, group_users: list[User] | None, username: str) -> list[User] | None:
    match choice:
        case 1:
            return create_group_options(user, user_details, 1, friend_add_condition, friends_list, group_users)
        case 2:
            choice_string = friend_add_condition(user_details, friends_list, user, username, True)

            if choice_string == "success":
                new_group_user: User | None = next((u for u in User.users if u.username == username), None)
                if new_group_user and group_users:
                    group_users.append(new_group_user)

                choice = int(input("\nNew friend sucessfully added to group members\n\n1. Enter new username\n2. Create group\n3. Go home\n\n"))
            else:
                choice = int(input(f"\nUsername @{username} doesn't exists!\n\n1. Try again\n2. Create group\n3. Go home\n\n"))

            return group_user_choices(user, user_details, friend_add_condition, friends_list, choice, group_users)
        case 3:
            return group_users
        case 4:
            user_details(user)

            return None
        case _:
            choice = int(input(f"\nInvalid option {choice}, try again!\n\n1. Enter username\n2. Add user @{username} to friend list\n3. Create group without other users\n4. Cancel and Go home"))

            return no_group_user_choices(user, user_details, friend_add_condition, friends_list, choice, group_users, username)

def create_group_options(user: User, user_details: UserDetailsFn, choice: int, friend_add_condition: FriendAddConditionFn, friends_list: FriendsListFn, group_users: list[User] | None = None) -> list[User] | None:
    if group_users is None:
        group_users = []

    match choice:
        case 1:
            new_user = input("\nEnter new username: ")

            if any(u.username == new_user for u in group_users):
                choice = int(input(f"\nUsername @{new_user} already part of potential members!!\n\n1. Enter another user\n2. Create group\n3. Cancel and Go home\n\n"))

                return group_user_choices(user, user_details, friend_add_condition, friends_list, choice, group_users)
            elif any(f["username"] == new_user for f in user.friends):
                new_group_user: User | None = next((u for u in User.users if u.username == new_user), None)

                if new_group_user:
                    group_users.append(new_group_user)

                choice = int(input("\nUsername successfully added!!\n\n1. Enter another user\n2. Create group\n3. Cancel and Go home\n\n"))

                return group_user_choices(user, user_details, friend_add_condition, friends_list, choice, group_users)
            else:
                choice = int(input(f"\nUsername @{new_user} not part of friends!!\n\n1. Try again\n2. Add user @{new_user} to friend list\n3. Create group\n4. Cancel and Go home\n\n"))

                return no_group_user_choices(user, user_details, friend_add_condition, friends_list, choice, group_users, new_user)
        case 2:
            return group_users
        case _:
            choice = int(input(f"\n{choice} not of the options available!\n\n1. Yes (Enter new users)\n2. No (Create group without users)\n\n"))

            return create_group_options(user, user_details, choice, friend_add_condition, friends_list, group_users)

def friend_message_error(choice: int, user_details: UserDetailsFn, user: User, friend_add_condition, friends_list, groups_list: GroupsListFn, room: MultiChatRoom, group_name: str):
    match choice:
        case 1:
            enter_chat(user_details, friends_list, user, friend_add_condition, groups_list, room, group_name)
        case 2:
            user_details(user)
        case _:
            choice = int(input(f"\n{choice} not part of options available\n\n1. Try again\n2. Go home\n\n"))

            friend_message_error(choice, user_details, friends_list, user, friend_add_condition, groups_list, room, group_name)

def enter_chat(user_details: UserDetailsFn, user: User, friend_add_condition, friends_list, groups_list: GroupsListFn, room: MultiChatRoom, group_name: str):
    message: str = input("\nNew message: ")

    response = post("http://127.0.0.1:8000/messages", json={"room_id": room.room_id, "u_id": user.id, "text": message})

    if not response.ok:
        print(f"\nError: {response.status_code} {response.text}")

        choice = int(input("\nUnable to enter new message to chat\n\n1. Try again\n2. Go home\n\n"))
        friend_message_error(choice, user_details, friends_list, user, friend_add_condition, groups_list, room, group_name)

    data = response.json()

    result_string = room.enter_chat_to_room(user.username, data["text"], data["time_stamp"])

    if result_string is not None:
        print(result_string)

    group_chat_details(user_details, user, friend_add_condition, friends_list, groups_list, room, group_name)

def add_group_member_action(user_details: UserDetailsFn, user: User, make_request: Callable[[User], Response] | None, success: str, friend_add_condition: FriendAddConditionFn, friends_list: FriendsListFn, groups_list: GroupsListFn, room: MultiChatRoom, group_name: str, username: str, action: Callable[[User, User], str], not_found_message: Callable[[str], str], require_friend: bool = True) -> None:
    if require_friend and not any(f["username"] == username for f in user.friends):
        print(not_found_message(username))
    else:
        target_user: User | None = next((u for u in User.users if u.username == username), None)

        if target_user:
            result_string: str = action(user, target_user)

            if result_string != "success":
                print(result_string)
            else:
                response = make_request(target_user)

                if not response.ok:
                    print(f"\nError: {response.status_code} {response.text}")
                else:
                    print(success)
        else:
            print(not_found_message(username))

    group_chat_details(user_details, user, friend_add_condition, friends_list, groups_list, room, group_name)

def add_user(user_details: UserDetailsFn, user: User, friend_add_condition: FriendAddConditionFn, friends_list: FriendsListFn, groups_list: GroupsListFn, room: MultiChatRoom, group_name: str) -> None:
    new_username: str = input("\nEnter new username: ")

    add_group_member_action(
        user_details,
        user,
        lambda target_user: post("http://127.0.0.1:8000/group-members", json={"u_id": target_user.id, "group_id": room.room_id}),
        "\nNew user successfully added to the group!",
        friend_add_condition,
        friends_list,
        groups_list,
        room,
        group_name,
        new_username,
        room.add_user_to_room,
        lambda name: f"\n@{name} not part of friend list, can't add to group!"
    )

def add_admin(user_details: UserDetailsFn, user: User, friend_add_condition: FriendAddConditionFn, friends_list: FriendsListFn, groups_list: GroupsListFn, room: MultiChatRoom, group_name: str) -> None:
    new_admin_username: str = input("\nEnter new admin username: ")

    add_group_member_action(
        user_details,
        user,
        lambda target_user: patch(f"http://127.0.0.1:8000/group-members/{room.room_id}/{target_user.id}", json={"u_id": target_user.id, "group_id": room.room_id, "role": "admin"}),
        "\nNew admin successfully added to the group!",
        friend_add_condition,
        friends_list,
        groups_list,
        room,
        group_name,
        new_admin_username,
        room.add_room_admin,
        lambda name: f"\n@{name} not a user!", require_friend=False
    )

def user_view_group_options(choice: int, user_details: UserDetailsFn, user: User, friend_add_condition: FriendAddConditionFn, friends_list: FriendsListFn, groups_list: GroupsListFn, room: MultiChatRoom, group_name: str) -> None:
    match choice:
        case 1:
            enter_chat(user_details, user, friend_add_condition, friends_list, groups_list, room, group_name)
        case 2:
            add_user(user_details, user, friend_add_condition, friends_list, groups_list, room, group_name)
        case 3:
            groups_list(user, user_details, friend_add_condition, friends_list, create_group, create_group_steps, group_chat_details, add_group_member_action)
        case 4:
            user_details(user)
        case _:
            choice = int(input(f"\n{choice} not part of options available!\n\n1. Enter chat to room\n2. Add a group member\n3. View group list\4. Go home\n\n"))

            user_view_group_options(choice, user_details, user, friend_add_condition, friends_list, groups_list, room, group_name)

def user_view_group_admin_options(choice, user_details: UserDetailsFn, user: User, friend_add_condition: FriendAddConditionFn, friends_list: FriendsListFn, groups_list: GroupsListFn, room: MultiChatRoom, group_name: str) -> None:
    match choice:
        case 1:
            enter_chat(user_details, user, friend_add_condition, friends_list, groups_list, room, group_name)
        case 2:
            add_admin(user_details, user, friend_add_condition, friends_list, groups_list, room, group_name)
        case 3:
            add_user(user_details, user, friend_add_condition, friends_list, groups_list, room, group_name)
        case 4:
            groups_list(user, user_details, friend_add_condition, friends_list, create_group, create_group_steps, group_chat_details, add_group_member_action)
        case 5:
            user_details(user)
        case _:
            choice = int(input(f"\n{choice} not part of options available!\n\n. Enter chat to room\n2. Add admin from group members\n3. Add a group member\n4. View group list\n5. Go home\n\n"))

            user_view_group_admin_options(choice, user_details, user, friend_add_condition, friends_list, groups_list, room, group_name)

def determine_users_exists(room: MultiChatRoom, user: User):
    room_users = room.users

    if room_users:
        user_group_object: GroupUser | None = next((u for u in room_users if u.username == user.username), None)

        return user_group_object
    else:
        return None

def determine_user_group_options(user_details: UserDetailsFn, user: User, friend_add_condition: FriendAddConditionFn, friends_list: FriendsListFn, groups_list: GroupsListFn, room: MultiChatRoom, group_name: str) -> None:
    user_group_object = determine_users_exists(room, user)

    if user_group_object is None:
        return None

    if user_group_object.role == "admin":
        choice = int(input("\n1. Enter chat to room\n2. Add admin from group members\n3. Add a group member\n4. View group list\n5. Go home\n\n"))

        user_view_group_admin_options(choice, user_details, user, friend_add_condition, friends_list, groups_list, room, group_name)
    else:
        choice = int(input("\n1. Enter chat to room\n2. Add a group member\n3. View group list\4. Go home\n\n"))

        user_view_group_options(choice, user_details, user, friend_add_condition, friends_list, groups_list, room, group_name)

    return None

def group_chat_details(user_details: UserDetailsFn, user: User, friend_add_condition: FriendAddConditionFn, friends_list: FriendsListFn, groups_list: GroupsListFn, room: MultiChatRoom, group_name: str):
    print(f"\nGroup Name: {group_name}")

    get_room_messages(room)
    room_messages = room.messages

    get_room_users(room)
    room_users = room.users

    if room_messages is not None:
        display_room_infos(room_messages, sort_key=lambda m: m.created_at, formatter=lambda i, m: f"[{m.created_at}] {m.username}: {m.text}", title="Messages")

    if room_users is not None:
        display_room_infos(room_users, sort_key=lambda u: u.role != "admin",formatter=lambda i, u: f"{i + 1}: {u.username}{' (admin)' if u.role == 'admin' else ''}", title="Users")

    determine_user_group_options(user_details, user, friend_add_condition, friends_list, groups_list, room, group_name)

def group_created_options(choice, user_details: UserDetailsFn, friend_add_condition: FriendAddConditionFn, friends_list: FriendsListFn, groups_list: GroupsListFn, user: User, room: MultiChatRoom, group_name: str) -> None:
    match choice:
        case 1:
            group_chat_details(user_details, user, friend_add_condition, friends_list, groups_list, room, group_name)
        case 2:
            groups_list(user, user_details, friend_add_condition, friends_list, create_group, create_group_steps, group_chat_details, add_group_member_action)
        case 3:
            user_details(user)
        case _:
            choice = int(input(f"\n{choice} not part of options available\n\n1. Enter group chat\n2. View group list\n3. Go home\n\n"))

            group_created_options(choice, user_details, friend_add_condition, friends_list, groups_list, user, room, group_name)


def unable_to_create_group(choice: int, user: User, user_details: UserDetailsFn, friend_add_condition: FriendAddConditionFn, friends_list: FriendsListFn, groups_list: GroupsListFn):
    match choice:
        case 1:
            group_name = input("\nEnter a group name: ")
            create_group_steps(user, user_details, friend_add_condition, friends_list, groups_list, group_name)
        case 2:
            user_details(user)
        case _:
            choice = int(input(f"{choice} choice not part of options availabe\n\n1. Try Again\n2. Go home\n\n"))

            unable_to_create_group(choice, user, user_details, friend_add_condition, friends_list, groups_list)


def create_group_steps(user: User, user_details: UserDetailsFn, friend_add_condition: FriendAddConditionFn, friends_list: FriendsListFn, groups_list: GroupsListFn, group_name: str):
    choice = int(input("\nDo you want to enter new users? \n\n1. Yes (Enter new users)\n2. No (Create group as only user)\n\n"))

    group_users = create_group_options(user, user_details, choice, friend_add_condition, friends_list)

    if group_users is not None:
        response = post("http://127.0.0.1:8000/groups", json={"group_name": group_name, "u_id": user.id})

        if not response.ok:
            print(f"\nError: {response.status_code} {response.text}")

            choice = int(input("\nUnable to create group\n\n1. Try Again\n2. Go home\n\n"))
            unable_to_create_group(choice, user, user_details, friend_add_condition, friends_list, groups_list)

        data = response.json()

        successful_members: list[User] = []

        for u in group_users:
            response = post("http://127.0.0.1:8000/group-members", json={"u_id": u.id, "group_id": data["group"]["id"]})

            if not response.ok:
                print(f"\nError: {response.status_code} {response.text}")
            else:
                successful_members.append(u)

        multi_room = user.create_multi_user_room(data["group"]["id"], group_name, successful_members)

        user.add_group(group_name, multi_room)

        choice = int(input("\nGroup successfully created!\n\n1. Enter group chat\n2. View group list\n3. Go home\n\n"))

        group_created_options(choice, user_details, friend_add_condition, friends_list, groups_list, user, multi_room, group_name)


def create_group(user: User, user_details: UserDetailsFn, friend_add_condition: FriendAddConditionFn, friends_list: FriendsListFn, groups_list: GroupsListFn) -> None:
    group_name = input("\nEnter a group name: ")

    create_group_steps(user, user_details, friend_add_condition, friends_list, groups_list, group_name)