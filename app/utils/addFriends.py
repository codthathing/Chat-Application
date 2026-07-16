from typing import cast
from models.Message import Message
from models.ChatRoom import DualChatRoom
from models.User import User
from checkers.types import UserDetailsFn, FriendsListFn

def friend_already_exists(choice: int, user: User, user_details: UserDetailsFn, friends_list: FriendsListFn, room: DualChatRoom) -> None:
    match choice:
        case 1:
            if not room.messages:
                pass
            else:
                sorted_messages: list[Message] = sorted(room.messages, key=lambda m: m.created_at)

                print("")

                for msg in sorted_messages:
                    print(f"[{msg.created_at}] {msg.username}: {msg.text}")

            choice = int(input("\n1. Enter new chat\n2. View friend list\n3. Go home\n\n"))

            friend_chat_options(user_details, friends_list, choice, user, room)
        case 2:
            add_friend(user, user_details, friends_list)
        case 3:
            user_details(user)
        case _:
            choice = int(input(f"\n{choice} not part of options available!\n\n1. View friend chat\n2. Go home\n\n"))

            friend_already_exists(choice, user, user_details, friends_list, room)

def friend_add_condition(user_details: UserDetailsFn, friends_list: FriendsListFn, user: User, friend: str) -> None:
    new_friend: User | None = next((u for u in User.users if u.username == friend), None)

    if new_friend:
        if any(f["username"] == friend for f in user.friends):
            mutual_room: DualChatRoom = cast("DualChatRoom", next((u["room"] for u in user.friends if u["username"] == friend), None))

            choice = int(input("\nUser already part of friend list!\n\n1. Visit friend chat\n2. Add a friend\n3. Go home\n\n"))

            friend_already_exists(choice, user, user_details, friends_list, mutual_room)
        else:
            mutual_room: DualChatRoom = user.create_dual_user_room(new_friend)
            user.add_friends(friend, mutual_room)

            choice = int(input("\nNew friend successfully added!\n\n1. Chat with friend\n2. Go home\n\n"))

            friend_exists(user_details, friends_list, choice, user, mutual_room)
    else:
        choice = int(input(f"\nUser @{friend} doesn't exists!\n\n1. Try again\n2. Go home\n\n"))

        no_friend_exists(user_details, friends_list, choice, user)


def add_friend(user: User, user_details: UserDetailsFn, friends_list: FriendsListFn) -> None:
    friend: str = input("\nEnter friend username: ")

    friend_add_condition(user_details, friends_list, user, friend)


def friend_chat_options(user_details: UserDetailsFn, friends_list: FriendsListFn, choice: int, user: User, room: DualChatRoom):
    match choice:
        case 1:
            new_friend_chat(user_details, friends_list, user, room)
        case 2:
            friends_list(user, user_details, add_friend, friend_chat_options, friend_add_condition)
        case 3:
            user_details(user)
        case _:
            choice = int(input(f"{choice} not part of options available!\n\n1. Enter new chat\n2. View friend list\n3. Go home\n\n"))

            friend_chat_options(user_details, friends_list, choice, user, room)


def new_friend_chat(user_details: UserDetailsFn, friends_list: FriendsListFn, user: User, room: DualChatRoom) -> None:
    message: str = input("\nNew message: ")

    room.enter_chat_to_room(user.username, message)

    if len(room.messages) > 0:
        sorted_messages: list[Message] = sorted(room.messages, key=lambda m: m.created_at)

        print("")

        for msg in sorted_messages:
            print(f"[{msg.created_at}] {msg.username}: {msg.text}")

    choice = int(input("\n1. Enter new chat\n2. View friend list\n3. Go home\n\n"))

    friend_chat_options(user_details, friends_list, choice, user, room)


def friend_exists(user_details: UserDetailsFn, friends_list: FriendsListFn, choice: int, user: User, room: DualChatRoom):
    match choice:
        case 1:
            new_friend_chat(user_details, friends_list, user, room)
        case 2:
            user_details(user)
        case _:
            choice = int(input(f"\n{choice} not part of options available!\n\n1. Chat with friend\n2. Go home\n\n"))

            friend_exists(user_details, friends_list, choice, user, room)


def no_friend_exists(user_details: UserDetailsFn, friends_list: FriendsListFn, choice: int, user: User):
    match choice:
        case 1:
            add_friend(user, user_details, friends_list)
        case 2:
            user_details(user)
        case _:
            choice = int(input(f"\n{choice} not part of options available!\n\n1. Try again\n2. Go home\n\n"))

            no_friend_exists(user_details, friends_list, choice, user)