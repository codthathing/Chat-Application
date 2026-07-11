from models.Message import Message
from models.ChatRoom import DualChatRoom
from models.User import User
from utils.types import UserDetailsFn, FriendsListFn


def friendAddCondition(userDetails: UserDetailsFn, friendsList: FriendsListFn, user: User, friend: str) -> None:
    newFriend: User | None = next((u for u in User.users if u.username == friend), None)

    if newFriend:
        mutualRoom: DualChatRoom = user.createDualUserRoom(newFriend)
        user.addFriends(friend, mutualRoom)

        choice = int(input("\nNew friend successfully added!\n\n1. Chat with friend\n2. Go home\n\n"))

        friendExists(userDetails, friendsList, choice, user, mutualRoom)
    else:
        choice = int(input(f"\nUser @{friend} doesn't exists!\n\n1. Try again\n2. Go home\n\n"))

        noFriendExists(userDetails, friendsList, choice, user)


def addFriend(user: User, userDetails: UserDetailsFn, friendsList: FriendsListFn) -> None:
    friend: str = input("\nEnter friend username: ")

    friendAddCondition(userDetails, friendsList, user, friend)


def friendChatOptions(userDetails: UserDetailsFn, friendsList: FriendsListFn, choice: int, user: User, room: DualChatRoom) -> None:
    match choice:
        case 1:
            newFriendChat(userDetails, friendsList, user, room)
        case 2:
            friendsList(user, userDetails, addFriend, friendChatOptions, friendAddCondition)
        case 3:
            userDetails(user)
        case _:
            choice = int(input(f"{choice} not part of options available!\n\n1. Enter new chat\n2. View friend list\n3. Go home\n\n"))

            return friendChatOptions(userDetails, friendsList, choice, user, room)


def newFriendChat(userDetails: UserDetailsFn, friendsList: FriendsListFn, user: User, room: DualChatRoom) -> None:
    message: str = input("\nNew message: ")

    room.enterChatToRoom(user.username, message)

    if len(room.messages) > 0:
        sorted_messages: list[Message] = sorted(room.messages, key=lambda m: m.created_at)

        print("")

        for msg in sorted_messages:
            print(f"[{msg.created_at}] {msg.username}: {msg.text}")

    choice = int(input("\n1. Enter new chat\n2. View friend list\n3. Go home\n\n"))

    friendChatOptions(userDetails, friendsList, choice, user, room)


def friendExists(userDetails: UserDetailsFn, friendsList: FriendsListFn, choice: int, user: User, room: DualChatRoom) -> None:
    match choice:
        case 1:
            newFriendChat(userDetails, friendsList, user, room)
        case 2:
            userDetails(user)
        case _:
            choice = int(input(f"\n{choice} not part of options available!\n\n1. Chat with friend\n2. Go home\n\n"))

            return friendExists(userDetails, friendsList, choice, user, room)


def noFriendExists(userDetails: UserDetailsFn, friendsList: FriendsListFn, choice: int, user: User) -> None:
    match choice:
        case 1:
            addFriend(user, userDetails, friendsList)
        case 2:
            userDetails(user)
        case _:
            choice = int(input(f"\n{choice} not part of options available!\n\n1. Try again\n2. Go home\n\n"))

            return noFriendExists(userDetails, friendsList, choice, user)