from models.User import User
from typing import Callable

def friendsList(user: User, userDetails: Callable[[User], None]) -> None:
    print("")

    for i, friend in enumerate(user.friends, start=1):
        print(f"{i}. {friend['username']}")

    choice = int(input("\n1. Visit friend chat\n2. Go home\n\n"))

    friendsListOption(userDetails, choice, user)

def friendsListOption(userDetails: Callable[[User], None], choice: int, user: User) -> None: 
    match choice:
        case 1:
            pass
        case 2:
            userDetails(user)
        case _:
            choice = int(input(f"{choice} not part of options available!\n\n1. View friend chat\n2.Go home\n\n"))

            return friendsListOption(userDetails, choice, user)