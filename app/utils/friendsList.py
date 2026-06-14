from models.User import User
from typing import Callable

def friendsList(user: User, userDetails: Callable[[User], None], addFriend: Callable[[User, Callable[[User], None]], None]) -> None:
    print("")

    if len(user.friends) > 0:
        for i, friend in enumerate(user.friends, start=1):
            print(f"{i}. {friend['username']}")

        choice = int(input("\n1. Visit friend chat\n2. Go home\n\n"))
        friendsListOption(userDetails, choice, user)
    else:
        choice = int(input("You currently have no friends!\n\n1. Add a friend\n2.Go home\n\n"))
        friendsListEmpty(userDetails, addFriend, choice, user)

def friendsListOption(userDetails: Callable[[User], None], choice: int, user: User) -> None: 
    match choice:
        case 1:
            # friendUsername = int(input("\nEnter friend username: "))
            pass
        case 2:
            userDetails(user)
        case _:
            choice = int(input(f"\n{choice} not part of options available!\n\n1. View friend chat\n2.Go home\n\n"))

            return friendsListOption(userDetails, choice, user)
        
def friendsListEmpty(userDetails: Callable[[User], None], addFriend: Callable[[User, Callable[[User], None]], None], choice: int, user: User) -> None:
    match choice:
        case 1:
            addFriend(user, userDetails)
        case 2:
            userDetails(user)
        case _:
            choice = int(input(f"\n{choice} not part of options available!\n\n1. Add a friend\n2.Go home\n\n"))

            return friendsListEmpty(userDetails, addFriend, choice, user)