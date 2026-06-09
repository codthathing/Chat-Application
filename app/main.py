from models.User import User
from schemas.UsersRoomSchema import UsersRoomSchema
import argparse
from sys import exit

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

            userChatSchema = UsersRoomSchema()
            
            return userChatSchema.createUser(username, email)
        elif choice.lower() == "n":
            exit("\nThanks for using Freechat!")
    
    user = verifyOption(user)


def userDetails(user: User) -> None:
    choice: int = int(input(f"\nUsername: {user.username}\nEmail: {user.email}\n\n1. View friends list\n2. Add a new friend\n3. Create a group\n4. User settings\n5. Log out\n\n"))
    
    if choice not in range(1, 6):
        print("\nOption not available!")

        userDetails(user)

if user:
    userDetails(user)