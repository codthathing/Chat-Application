from typing import cast

from models.ChatRoom import MultiChatRoom, ChatRoom
from models.User import User
from utils.types import GroupChatDetailsFn, UserDetailsFn, CreateGroupFn, AddGroupMemberActionFn

def no_group_list_exists(choice: int, user: User, userDetails: UserDetailsFn, create_group: CreateGroupFn, add_group_member_action: AddGroupMemberActionFn):
    match choice:
        case 1:
            create_group(user, userDetails)
        case 2:
            group_name = int(input("\nEnter group chat name: "))

            room = cast("MultiChatRoom | None", next((r for r in ChatRoom.chatrooms if isinstance(r, MultiChatRoom) and r.group_name == group_name), None))

            if room:
                add_group_member_action(userDetails, user, room, group_name, user.username, room.addUserToRoom, lambda name: f"\n@{name} not a user, can't add to group!")
            else:
                choice = int(input(f"\nGroup chat with {group_name} does not exist!\n\n1. Create group chat {group_name}\n2. Send group chat request for {group_name}\n3. Go home\n\n"))
        case 3:
            userDetails(user)
        case _:
            choice = int(input(f"{choice} not part of the options available\n\n1. Create group chat\n2. Send group chat request\n3. Go home\n\n"))

            no_group_list_exists(choice, user, userDetails, create_group)

def group_list_exists(choice: int, user: User, userDetails: UserDetailsFn, create_group: CreateGroupFn, group_chat_details: GroupChatDetailsFn):
    match choice:
        case 1:
            group_name = int(input("\nEnter group chat name: "))

            if group_name in user.groups:
                room = cast("MultiChatRoom | None", next((r for r in ChatRoom.chatrooms if isinstance(r, MultiChatRoom) and r.group_name == group_name), None))

                group_chat_details(userDetails, user, room, group_name)
            else:
                choice = int(input(f"\nGroup chat with {group_name} does not exist in your list!\n\n1. Create group chat {group_name}\n2. Send group chat request for {group_name}\n3. Go home\n\n"))
        case 2:
            create_group(user, userDetails)
        case 3:
            userDetails(user)
        case _:
            choice = int(input(f"{choice} not part of the options available\n\n1. Visit group chat\n2.Create group chat\n3. Go home\n\n"))

            group_list_exists(choice, user, userDetails, create_group, group_chat_details)

def groups_list(user: User, userDetails: UserDetailsFn, create_group: CreateGroupFn, group_chat_details: GroupChatDetailsFn, add_group_member_action: AddGroupMemberActionFn):
    if user.groups:
        for i, g in enumerate(user.groups, start=1):
            print(f"{i}. {g}")

        choice = int(input("\n1. Visit group chat\n2.Create group chat\n3. Go home\n\n"))

        group_list_exists(choice, user, userDetails, create_group, group_chat_details)
    else:
        choice = int(input("\nYou're currently not in a group\n\n1. Create group chat\n2. Send group chat request\n3. Go home\n\n"))

        no_group_list_exists(choice, user, userDetails, create_group, add_group_member_action)