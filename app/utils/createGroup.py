from models.User import User

def create_group_options(choice) -> list[User]:
    match choice:
        case 1:
            new_user = input("Enter new username: ")

            new_group_user: User | None = next((u for u in User.users if u.username == new_user), None)

            if new_group_user:
                pass
            else:
                pass
        case 2:
            pass
        case _:
            choice = int(input(""))

            return  create_group_options(choice)

def create_group(user: User) -> None:
    group_name = input("Enter a group name: ")

    choice = int(input("Do you want to enter new users? \n\n1. Yes (Enter new users)\n2. No (Create group as only user)\n\n"))

    group_users = create_group_options(choice)

    multi_room = user.createMultiUserRoom(group_users)