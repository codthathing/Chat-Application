from models.ChatRoom import DualChatRoom
from models.User import User
from typing import Callable
from utils.friendsList import friendsList

def addFriend(user: User, userDetails: Callable[[User], None]) -> None:
    friend: str = input("\nEnter friend username: ")

    newFriend: User | None = next((u for u in User.users if u.username == friend), None)

    if newFriend:
        mutualRoom: DualChatRoom = user.createDualUserRoom(newFriend)
        user.addFriends(friend, mutualRoom)

        choice = int(input("\nNew friend successfully added!\n\n1. Chat with friend\n2. Go home\n\n"))

        friendExists(userDetails, choice, user, mutualRoom)
    else:
        choice = int(input(f"\nUser @{friend} doesn't exists!\n\n1. Try again\n2. Go home\n\n"))

        noFriendExists(userDetails, choice, user)

def friendChatOptions(userDetails: Callable[[User], None], choice: int, user: User, room: DualChatRoom) -> None:
    match choice:
        case 1:
            newFriendChat(userDetails, user, room)
        case 2:
            friendsList(user, userDetails, addFriend)
        case 3:
            userDetails(user)
        case _:
            choice = int(input(f"{choice} not part of options available!\n\n1. Enter new chat\n2. View friend list\n3.Go home\n\n"))

            return friendChatOptions(userDetails, choice, user, room)

def newFriendChat(userDetails: Callable[[User], None], user: User, room: DualChatRoom) -> None:
    message: str = input("\nNew message: ")

    room.enterChatToRoom(user, message)

    # Display all the messages

    choice = int(input("\n1. Enter new chat\n2. View friend list\n3. Go home\n\n"))

    friendChatOptions(userDetails, choice, user, room)

def friendExists(userDetails: Callable[[User], None], choice: int, user: User, room: DualChatRoom) -> None:
    match choice:
        case 1:
            newFriendChat(userDetails, user, room)
        case 2:
            userDetails(user)
        case _:
            choice = int(input(f"\n{choice} not part of options available!\n\n1. Chat with friend\n2.Go home\n\n"))

            return friendExists(userDetails, choice, user, room)

def noFriendExists(userDetails: Callable[[User], None], choice: int, user: User) -> None:
    match choice:
        case 1:
            addFriend(user, userDetails)
        case 2:
            userDetails(user)
        case _:
            choice = int(input(f"\n{choice} not part of options available!\n\n1. Try again\n2.Go home\n\n"))

            return noFriendExists(userDetails, choice, user)