from models.ChatRoom import DualChatRoom
from models.User import User
from models.Message import Message
from checkers.types import UserDetailsFn, AddFriendFn, FriendChatOptionsFn, FriendAddConditionFn


def friends_list(user: User, user_details: UserDetailsFn, add_friend: AddFriendFn, friend_chat_options: FriendChatOptionsFn, friend_add_condition: FriendAddConditionFn) -> None:
    print("")

    if len(user.friends) > 0:
        for i, friend in enumerate(user.friends, start=1):
            print(f"{i}. {friend['username']}")

        choice = int(input("\n1. Visit friend chat\n2. Add a friend\n3. Go home\n\n"))
        friends_list_option(user_details, friend_chat_options, friend_add_condition, add_friend, choice, user)
    else:
        choice = int(input("You currently have no friends!\n\n1. Add a friend\n2. Go home\n\n"))
        friends_list_empty(user_details, add_friend, choice, user)


def not_friends_options(user_details: UserDetailsFn, friend_chat_options: FriendChatOptionsFn, friend_add_condition: FriendAddConditionFn, add_friend: AddFriendFn, user: User, choice: int, friend_username: str):
    match choice:
        case 1:
            friends_list_option(user_details, friend_chat_options, friend_add_condition, add_friend, choice, user)
        case 2:
            friend_add_condition(user_details, friends_list, user, friend_username)
        case 3:
            user_details(user)
        case _:
            choice = int(input(f"\nUser @{friend_username} not part of friends list!\n\n1. Try again\n2. Add @{friend_username} to friends list\n3. Go home\n\n"))

            not_friends_options(user_details, friend_chat_options, friend_add_condition, add_friend, user, choice, friend_username)


def friends_list_option(user_details: UserDetailsFn, friend_chat_options: FriendChatOptionsFn, friend_add_condition: FriendAddConditionFn, add_friend: AddFriendFn, choice: int, user: User):
    match choice:
        case 1:
            friend_username: str = input("\nEnter friend username: ")

            room: DualChatRoom | None = next((r["room"] for r in user.friends if r["username"] == friend_username), None)

            if room:
                if room.messages:
                    sorted_messages: list[Message] = sorted(room.messages, key=lambda m: m.created_at)

                    print("")

                    for msg in sorted_messages:
                        print(f"[{msg.created_at}] {msg.username}: {msg.text}")

                choice = int(input("\n1. Enter new chat\n2. View friend list\n3. Go home\n\n"))

                friend_chat_options(user_details, friends_list, choice, user, room)
            else:
                choice = int(input(f"\nUser @{friend_username} not part of friends list!\n\n1. Try again\n2. Add @{friend_username} to friends list\n3. Go home\n\n"))

                not_friends_options(user_details, friend_chat_options, friend_add_condition, add_friend, user, choice, friend_username)
        case 2:
            add_friend(user, user_details, friends_list)
        case 3:
            user_details(user)
        case _:
            choice = int(input(f"\n{choice} not part of options available!\n\n1. View friend chat\n2. Go home\n\n"))

            friends_list_option(user_details, friend_chat_options, friend_add_condition, add_friend, choice, user)


def friends_list_empty(user_details: UserDetailsFn, add_friend: AddFriendFn, choice: int, user: User):
    match choice:
        case 1:
            add_friend(user, user_details, friends_list)
        case 2:
            user_details(user)
        case _:
            choice = int(input(f"\n{choice} not part of options available!\n\n1. Add a friend\n2. Go home\n\n"))

            friends_list_empty(user_details, add_friend, choice, user)