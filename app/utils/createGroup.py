from typing import Callable, TypeVar, Any
from models.ChatRoom import MultiChatRoom
from models.User import User, GroupUser
from checkers.types import UserDetailsFn, GroupsListFn, FriendAddConditionFn, FriendsListFn

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
            friend_add_condition(user_details, friends_list, user, username)

            return None
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

            if any(f["username"] == new_user for f in user.friends):
                new_group_user: User | None = next((u for u in User.users if u.username == new_user), None)

                if new_group_user:
                    group_users.append(new_group_user)

                choice = int(input("\nUsername successfully added!!\n\n1. Enter another user\n2. Create group\n3. Cancel and Go home\n\n"))

                return group_user_choices(user, user_details, friend_add_condition, friends_list, choice, group_users)
            else:
                choice = int(input(f"\nUsername @{new_user} not part of friends!!\n\n1. Try again\n2. Add user @{new_user} to friend list\n3. Create group without other users\n4. Cancel and Go home\n\n"))

                return no_group_user_choices(user, user_details, friend_add_condition, friends_list, choice, group_users, new_user)
        case 2:
            return group_users
        case _:
            choice = int(input(f"\n{choice} not of the options available!\n\n1. Yes (Enter new users)\n2. No (Create group without users)\n\n"))

            return create_group_options(user, user_details, choice, friend_add_condition, friends_list, group_users)

def enter_chat(user_details: UserDetailsFn, user: User, friend_add_condition, friends_list, groups_list: GroupsListFn, room: MultiChatRoom, group_name: str):
    message: str = input("\nNew message: ")

    room.enter_chat_to_room(user.username, message)

    group_chat_details(user_details, user, friend_add_condition, friends_list, groups_list, room, group_name)

def add_group_member_action(user_details: UserDetailsFn, user: User, friend_add_condition: FriendAddConditionFn, friends_list: FriendsListFn, groups_list: GroupsListFn, room: MultiChatRoom, group_name: str, username: str, action: Callable[[User, User], str], not_found_message: Callable[[str], str], require_friend: bool = True) -> None:
    if require_friend and not any(f["username"] == username for f in user.friends):
        print(not_found_message(username))
    else:
        target_user: User | None = next((u for u in User.users if u.username == username), None)

        if target_user:
            result_string: str = action(user, target_user)
            print(result_string)
        else:
            print(not_found_message(username))

    group_chat_details(user_details, user, friend_add_condition, friends_list, groups_list, room, group_name)


def add_user(user_details: UserDetailsFn, user: User, friend_add_condition: FriendAddConditionFn, friends_list: FriendsListFn, groups_list: GroupsListFn, room: MultiChatRoom, group_name: str) -> None:
    new_username: str = input("\nEnter new username: ")

    add_group_member_action(user_details, user, friend_add_condition, friends_list, groups_list, room, group_name, new_username, room.add_user_to_room, lambda name: f"\n@{name} not part of friend list, can't add to group!")

def add_admin(user_details: UserDetailsFn, user: User, friend_add_condition: FriendAddConditionFn, friends_list: FriendsListFn, groups_list: GroupsListFn, room: MultiChatRoom, group_name: str) -> None:
    new_admin_username: str = input("\nEnter new admin username: ")

    add_group_member_action(user_details, user, friend_add_condition, friends_list, groups_list, room, group_name, new_admin_username, room.add_room_admin, lambda name: f"\n@{name} not a user!", require_friend=False)

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

def determine_user_group_options(user_details: UserDetailsFn, user: User, friend_add_condition: FriendAddConditionFn, friends_list: FriendsListFn, groups_list: GroupsListFn, room: MultiChatRoom, group_name: str) -> None:
    user_group_object: GroupUser | None = next((u for u in room.users if u.username == user.username), None)

    if not user_group_object:
        return

    if user_group_object.room_status == "admin":
        choice = int(input("\n1. Enter chat to room\n2. Add admin from group members\n3. Add a group member\n4. View group list\n5. Go home\n\n"))

        user_view_group_admin_options(choice, user_details, user, friend_add_condition, friends_list, groups_list, room, group_name)
    else:
        choice = int(input("\n1. Enter chat to room\n2. Add a group member\n3. View group list\4. Go home\n\n"))

        user_view_group_options(choice, user_details, user, friend_add_condition, friends_list, groups_list, room, group_name)

def display_room_infos(title: str, items: list[T], sort_key: Callable[[T], Any], formatter: Callable[[int, T], str]) -> None:
    if len(items) == 0:
        return

    print(f"\n{title}: ")

    sorted_items = sorted(items, key=sort_key)

    for i, item in enumerate(sorted_items):
        print(formatter(i, item))

def group_chat_details(user_details: UserDetailsFn, user: User, friend_add_condition: FriendAddConditionFn, friends_list: FriendsListFn, groups_list: GroupsListFn, room: MultiChatRoom, group_name: str):
    print(f"\nGroup Name: {group_name}")
    display_room_infos("Users", room.users, sort_key=lambda u: u.room_status != "admin",formatter=lambda i, u: f"{i + 1}: {u.username}{' (admin)' if u.room_status == 'admin' else ''}")
    display_room_infos("Messages", room.messages, sort_key=lambda m: m.created_at,formatter=lambda i, m: f"[{m.created_at}] {m.username}: {m.text}")

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

def create_group_steps(user: User, user_details: UserDetailsFn, friend_add_condition: FriendAddConditionFn, friends_list: FriendsListFn, groups_list: GroupsListFn, group_name: str):
    choice = int(input("\nDo you want to enter new users? \n\n1. Yes (Enter new users)\n2. No (Create group as only user)\n\n"))

    group_users = create_group_options(user, user_details, choice, friend_add_condition, friends_list)

    if group_users is not None:
        multi_room = user.create_multi_user_room(group_name, group_users)

        user.add_group(group_name)

        choice = int(input("\nGroup successfully created!\n\n1. Enter group chat\n2. View group list\n3. Go home\n\n"))

        group_created_options(choice, user_details, friend_add_condition, friends_list, groups_list, user, multi_room, group_name)

def create_group(user: User, user_details: UserDetailsFn, friend_add_condition: FriendAddConditionFn, friends_list: FriendsListFn, groups_list: GroupsListFn) -> None:
    group_name = input("\nEnter a group name: ")

    create_group_steps(user, user_details, friend_add_condition, friends_list, groups_list, group_name)