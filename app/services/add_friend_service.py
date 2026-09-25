from typing import cast
from app.models.chatroom_model import DualChatRoom
from app.models.user_model import User
from app.checkers.types import UserDetailsFn, FriendsListFn
from requests import post
from app.utils.display_mutual_messages import display_mutual_messages


def friend_already_exists(choice: int, user: User, user_details: UserDetailsFn, friends_list: FriendsListFn, room: DualChatRoom) -> None:
    match choice:
        case 1:
            display_mutual_messages(user, user_details, friends_list, room)
        case 2:
            add_friend(user, user_details, friends_list)
        case 3:
            user_details(user)
        case _:
            choice = int(input(f"\n{choice} not part of options available!\n\n1. View friend chat\n2. Go home\n\n"))

            friend_already_exists(choice, user, user_details, friends_list, room)

def friend_add_condition(user_details: UserDetailsFn, friends_list: FriendsListFn, user: User, friend: str, group: bool = False) -> None | str:
    new_friend: User | None = next((u for u in User.users if u.username == friend), None)

    if new_friend:
        if any(f["username"] == friend for f in user.friends):
            mutual_room: DualChatRoom = cast("DualChatRoom", next((u["room"] for u in user.friends if u["username"] == friend), None))

            choice = int(input("\nUser already part of friend list!\n\n1. Visit friend chat\n2. Add a friend\n3. Go home\n\n"))

            friend_already_exists(choice, user, user_details, friends_list, mutual_room)

            return None
        else:
            friend_id: str = new_friend.id
            u_id = user.id

            response = post("http://127.0.0.1:8000/friends", json={"friend_id": friend_id, "u_id": u_id})

            if not response.ok:
                print(f"\nError: {response.status_code} {response.text}")

                choice = int(input("\nUnable to create friend\n\n1. Try Again\n2. Go home\n\n"))
                no_friend_exists(user_details, friends_list, choice, user)

            data = response.json()

            mutual_room: DualChatRoom = user.create_dual_user_room(data["room_id"], new_friend)
            user.add_friends(friend, mutual_room)

            if not group:
                choice = int(input("\nNew friend successfully added!\n\n1. Chat with friend\n2. Go home\n\n"))

                friend_exists(user_details, friends_list, choice, user, mutual_room)

                return None
            else:
                return "success"
    else:
        if not group:
            choice = int(input(f"\nUser @{friend} doesn't exists!\n\n1. Try again\n2. Go home\n\n"))

            no_friend_exists(user_details, friends_list, choice, user)

            return None
        else:
            return "fail"


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


def friend_message_error(choice: int, user_details: UserDetailsFn, friends_list: FriendsListFn, user: User, room: DualChatRoom):
    match choice:
        case 1:
            new_friend_chat(user_details, friends_list, user, room)
        case 2:
            user_details(user)
        case _:
            choice = int(input(f"\n{choice} not part of options available\n\n1. Try again\n2. Go home\n\n"))

            friend_message_error(choice, user_details, friends_list, user, room)


def new_friend_chat(user_details: UserDetailsFn, friends_list: FriendsListFn, user: User, room: DualChatRoom) -> None:
    message: str = input("\nNew message: ")

    response = post("http://127.0.0.1:8000/messages", json={"room_id": room.room_id, "u_id": user.id, "text": message})

    if not response.ok:
        print(f"\nError: {response.status_code} {response.text}")

        choice = int(input("\nUnable to enter new message to chat\n\n1. Try again\n2. Go home\n\n"))
        friend_message_error(choice, user_details, friends_list, user, room)

    data = response.json()

    result_string = room.enter_chat_to_room(user.username, data["text"], data["time_stamp"])

    if result_string is not None:
        print(result_string)

    display_mutual_messages(user, user_details, friends_list, room)


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