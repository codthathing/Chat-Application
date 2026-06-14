from models.User import User
from utils.addFriends import addFriend
from utils.friendsList import friendsList
import argparse
from sys import exit

users: list[dict[str, str]] = [
    { "username": "pheezy", "email": "akinwunmiolusegun277@gmail.com" },
    { "username": "fola_creator", "email": "fola.creator@yahoo.com" },
    { "username": "boyoyo", "email": "ifeanyi.ogbonaya@gmail.com" },
]

for u in users:
    User(u["username"], u["email"])

parser = argparse.ArgumentParser("Chat application operations")
parser.add_argument("-u", "--username", metavar="username", dest="username", required=True, help="The current username")

args: argparse.Namespace = parser.parse_args()

user: User | None = next((u for u in User.users if u.username == args.username), None)

if not user:
    choice: str = input("No user account found, do you want to create an account? (Y/N) ")

    def verifyOption(userObject: User | None) -> User | None:
        global choice

        if choice.lower() not in ["y", "n"]:
            choice = input(f"\n{choice.upper()} not an option! Do you want to create an account? (Y/N) ")

            return verifyOption(userObject)
        elif choice.lower() == "y":
            username: str = input("\nUsername (a-Z, 0-9, _): ")
            email: str = input("Email: ")
            
            return User(username, email)
        elif choice.lower() == "n":
            exit("\nThanks for using Freechat!")
    
    user = verifyOption(user)


def userOptions(choice: int, user: User) -> None:
    match choice:
        case 1:
            friendsList(user, userDetails, addFriend)
        case 2:
            addFriend(user, userDetails)
        case 6:
            exit("\nThanks for using Freechat!")
        case _:
            print("\nOption not available!")

            userDetails(user)

def userDetails(user: User) -> None:
    choice: int = int(input(f"\nUsername: {user.username}\nEmail: {user.email}\n\n1. View friends list\n2. Add a new friend\n3. Create a group\n4. View group list\n5. User settings\n6. Log out\n\n"))

    userOptions(choice, user)
        
if user:
    userDetails(user)