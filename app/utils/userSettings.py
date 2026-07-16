from checkers.types import UserDetailsFn
from models.User import User

def user_settings_option(choice: int, user: User, user_details: UserDetailsFn):
    match choice:
        case 1:
            new_username = input("\nEnter new username: ")

            username_response = user.update_username(new_username)

            print(f"\n{username_response}")

            user_settings(user, user_details)
        case 2:
            new_email = input("\nEnter new email: ")

            email_response = user.update_email(new_email)

            print(f"\n{email_response}")

            user_settings(user, user_details)
        case 3:
            user_details(user)
        case _:
            choice = int(input(f"\n{choice} not part of options available\n\n1. Change username\n2. Update account email\n3. Go home\n\n"))

            user_settings_option(choice, user, user_details)

def user_settings(user: User, user_details: UserDetailsFn):
    choice = int(input(f"\nUsername: {user.username}\nEmail: {user.email}\n\n1. Change username\n2. Update account email\n3. Go home\n\n"))

    user_settings_option(choice, user, user_details)