from models.ChatRoom import DualChatRoom
from models.User import User
from models.Message import Message
from utils.types import UserDetailsFn, AddFriendFn, FriendChatOptionsFn, FriendAddConditionFn


def friendsList(user: User, userDetails: UserDetailsFn, addFriend: AddFriendFn, friendChatOptions: FriendChatOptionsFn, friendAddCondition: FriendAddConditionFn) -> None:
    print("")

    if len(user.friends) > 0:
        for i, friend in enumerate(user.friends, start=1):
            print(f"{i}. {friend['username']}")

        choice = int(input("\n1. Visit friend chat\n2. Add a friend\n3. Go home\n\n"))
        friendsListOption(userDetails, friendChatOptions, friendAddCondition, choice, user)
    else:
        choice = int(input("You currently have no friends!\n\n1. Add a friend\n2. Go home\n\n"))
        friendsListEmpty(userDetails, addFriend, choice, user)


def notFriendsOptions(userDetails: UserDetailsFn, friendChatOptions: FriendChatOptionsFn, friendAddCondition: FriendAddConditionFn, user: User, choice: int, friendUsername: str):
    match choice:
        case 1:
            friendsListOption(userDetails, friendChatOptions, friendAddCondition, choice, user)
        case 2:
            friendAddCondition(userDetails, friendsList, user, friendUsername)
        case 3:
            userDetails(user)
        case _:
            choice = int(input(f"\nUser @{friendUsername} not part of friends list!\n\n1. Try again\n2. Add @{friendUsername} to friends list\n3. Go home\n\n"))

            notFriendsOptions(userDetails, friendChatOptions, friendAddCondition, user, choice, friendUsername)


def friendsListOption(userDetails: UserDetailsFn, friendChatOptions: FriendChatOptionsFn, friendAddCondition: FriendAddConditionFn, choice: int, user: User):
    match choice:
        case 1:
            friendUsername: str = input("\nEnter friend username: ")

            room: DualChatRoom | None = next((r["room"] for r in user.friends if r["username"] == friendUsername), None)

            if room:
                if room.messages:
                    sorted_messages: list[Message] = sorted(room.messages, key=lambda m: m.created_at)

                    print("")

                    for msg in sorted_messages:
                        print(f"[{msg.created_at}] {msg.username}: {msg.text}")

                choice = int(input("\n1. Enter new chat\n2. View friend list\n3. Go home\n\n"))

                friendChatOptions(userDetails, friendsList, choice, user, room)
            else:
                choice = int(input(f"\nUser @{friendUsername} not part of friends list!\n\n1. Try again\n2. Add @{friendUsername} to friends list\n3. Go home\n\n"))

                notFriendsOptions(userDetails, friendChatOptions, friendAddCondition, user, choice, friendUsername)
        case 2:
            userDetails(user)
        case _:
            choice = int(input(f"\n{choice} not part of options available!\n\n1. View friend chat\n2. Go home\n\n"))

            friendsListOption(userDetails, friendChatOptions, friendAddCondition, choice, user)


def friendsListEmpty(userDetails: UserDetailsFn, addFriend: AddFriendFn, choice: int, user: User):
    match choice:
        case 1:
            addFriend(user, userDetails, friendsList)
        case 2:
            userDetails(user)
        case _:
            choice = int(input(f"\n{choice} not part of options available!\n\n1. Add a friend\n2. Go home\n\n"))

            friendsListEmpty(userDetails, addFriend, choice, user)