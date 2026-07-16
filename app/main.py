from models.User import User
from utils.addFriends import add_friend, friend_chat_options, friend_add_condition
from utils.createGroup import create_group, group_chat_details, add_group_member_action, create_group_steps
from utils.friendsList import friends_list
import argparse
from sys import exit
from utils.groupsList import groups_list
from utils.userSettings import user_settings

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

    def verify_option(user_object: User | None) -> User | None:
        global choice

        if choice.lower() not in ["y", "n"]:
            choice = input(f"\n{choice.upper()} not an option! Do you want to create an account? (Y/N) ")

            return verify_option(user_object)
        elif choice.lower() == "y":
            username: str = input("\nUsername (a-Z, 0-9, _): ")
            email: str = input("Email: ")
            
            return User(username, email)
        elif choice.lower() == "n":
            exit("\nThanks for using Freechat!")
        return None

    user = verify_option(user)


def user_options(options_choice: int, user_options_profile: User) -> None:
    match options_choice:
        case 1:
            friends_list(user_options_profile, user_details, add_friend, friend_chat_options, friend_add_condition)
        case 2:
            add_friend(user_options_profile, user_details, friends_list)
        case 3:
            create_group(user_options_profile, user_details, friend_add_condition, friends_list, groups_list)
        case 4:
            groups_list(user_options_profile, user_details, friend_add_condition, friends_list, create_group, create_group_steps, group_chat_details, add_group_member_action)
        case 5:
            user_settings(user_options_profile, user_details)
        case 6:
            exit("\nThanks for using Freechat!")
        case _:
            print("\nOption not available!")

            user_details(user_options_profile)

def user_details(user_profile: User) -> None:
    user_choice: int = int(input(f"\nUsername: {user_profile.username}\nEmail: {user_profile.email}\n\n1. View friends list\n2. Add a new friend\n3. Create a group\n4. View group list\n5. User settings\n6. Log out\n\n"))

    user_options(user_choice, user_profile)
        
if user:
    user_details(user)