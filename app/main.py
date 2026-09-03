from app.models.User import User
from app.utils.addFriends import add_friend, friend_chat_options, friend_add_condition
from app.utils.createGroup import create_group, group_chat_details, add_group_member_action, create_group_steps
from app.utils.friendsList import friends_list
import argparse
from sys import exit
from app.utils.groupsList import groups_list
from app.utils.userSettings import user_settings
from app.utils.getUser import get_user
from requests import get

users = get("http://127.0.0.1:8000/users").json()

for u in users:
    User(u["id"], u["username"], u["email"])

parser = argparse.ArgumentParser("Chat application operations")
parser.add_argument("-u", "--username", metavar="username", dest="username", required=True, help="The current username")

args: argparse.Namespace = parser.parse_args()

user: User | None = get_user(args.username)

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