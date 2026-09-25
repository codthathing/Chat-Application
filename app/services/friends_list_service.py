from app.models.chatroom_model import DualChatRoom
from app.models.user_model import User
from app.checkers.types import UserDetailsFn, AddFriendFn, FriendChatOptionsFn, FriendAddConditionFn
from app.utils.get_room_messages import get_room_messages
from app.utils.display_mutual_messages import display_mutual_messages


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
            friend_add_condition(user_details, friends_list, user, friend_username, False)
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
                get_room_messages(room)
                display_mutual_messages(user, user_details, friends_list, room)
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