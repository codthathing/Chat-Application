from requests import patch

from app.checkers.types import UserDetailsFn
from app.models.user_model import User

def user_settings_option(choice: int, user: User, user_details: UserDetailsFn):
    match choice:
        case 1:
            new_username = input("\nEnter new username: ")

            username_response = user.update_username(new_username)

            if username_response == "success":
                response = patch(f"http://127.0.0.1:8000/users/username/{user.id}", json={"username": new_username, "u_id": user.id})

                if not response.ok:
                    print(f"\nUsername {new_username} not updated!")
                else:
                    print("\nUsername successfully changed!")
            else:
                print(username_response)

            user_settings(user, user_details)
        case 2:
            new_email = input("\nEnter new email: ")

            email_response = user.update_email(new_email)

            if email_response == "success":
                response = patch(f"http://127.0.0.1:8000/users/email/{user.id}", json={"email": new_email, "u_id": user.id})

                if not response.ok:
                    print(f"\nEmail {new_email} not updated!")
                else:
                    print("\nEmail successfully changed!")
            else:
                print(email_response)

            user_settings(user, user_details)
        case 3:
            user_details(user)
        case _:
            choice = int(input(f"\n{choice} not part of options available\n\n1. Change username\n2. Update account email\n3. Go home\n\n"))

            user_settings_option(choice, user, user_details)

def user_settings(user: User, user_details: UserDetailsFn):
    choice = int(input(f"\nUsername: {user.username}\nEmail: {user.email}\n\n1. Change username\n2. Update account email\n3. Go home\n\n"))

    user_settings_option(choice, user, user_details)