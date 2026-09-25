from app.models.user_model import User
from app.models.chatroom_model import DualChatRoom, MultiChatRoom
from requests import get, post


def create_user():
    username: str = input("\nUsername (a-Z, 0-9, _): ")
    email: str = input("Email: ")
    password: str = input("Password: ")

    try:
        User.validate(username, email)

        res = post("http://127.0.0.1:8000/auth", json={"username": username, "email": email, "password": password})

        if not res.ok:
            print(f"\nError: {res.status_code} {res.text}")

            choice = input(f"\nTry Again? (Y/N) ")
            return create_user() if choice.lower() == "y" else exit("\nThanks for using Freechat!")

        user_data = res.json()

        return User(user_data["id"], user_data["username"], user_data["email"])
    except ValueError as e:
        print(str(e))

        choice = input(f"\nTry Again? (Y/N) ")
        return create_user() if choice.lower() == "y" else exit("\nThanks for using Freechat!")


def verify_option(choice) -> User | None:
    match choice.lower():
        case "y":
            return create_user()
        case "n":
            exit("\nThanks for using Freechat!")
        case _:
            choice = input(f"\n{choice.upper()} not an option! Do you want to create an account? (Y/N) ")

            return verify_option(choice)


def get_user_details(user_name) -> User | None:
    user: User | None = next((u for u in User.users if u.username == user_name), None)

    if not user:
        choice: str = input("\nNo user account found, do you want to create an account? (Y/N) ")

        user = verify_option(choice)
    else:
        response = get(f"http://127.0.0.1:8000/users/me/{user.id}")

        if not response.ok:
            exit(f"\nError: {response.status_code} {response.text}")

        user_details = response.json()

        friends = user_details["friends"]
        groups = user_details["groups"]

        if friends:
            for f in friends:
                new_friend: User | None = next((u for u in User.users if u.id == f["id"]), None)

                if new_friend:
                    mutual_room: DualChatRoom = user.create_dual_user_room(f["room_id"], new_friend)
                    user.add_friends(f["username"], mutual_room)

        if groups:
            for g in groups:
                multi_room = MultiChatRoom(g["room_id"], g["group_name"])

                user.add_group(g["group_name"], multi_room)

    return user