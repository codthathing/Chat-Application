from typing import cast
from models.ChatRoom import MultiChatRoom, ChatRoom
from models.User import User
from utils.types import GroupChatDetailsFn, UserDetailsFn, CreateGroupFn, AddGroupMemberActionFn, CreateGroupStepsFn

def group_not_exists(choice: int, user: User, userDetails: UserDetailsFn, create_group: CreateGroupFn, create_group_steps: CreateGroupStepsFn, group_chat_details: GroupChatDetailsFn, add_group_member_action: AddGroupMemberActionFn, group_name: str):
    match choice:
        case 1:
            create_group_steps(user, userDetails, groups_list, group_name)
        case 2:
            groups_list(user, userDetails, create_group, create_group_steps, group_chat_details, add_group_member_action)
        case 3:
            userDetails(user)
        case _:
            choice = int(input(f"\n{choice} not part of the options available!\n\n1. Create group chat {group_name}\n2. View group list\n3. Go home\n\n"))

            group_not_exists(choice, user, userDetails, create_group, create_group_steps, group_chat_details, add_group_member_action, group_name)

def send_group_request(user: User, userDetails: UserDetailsFn, create_group: CreateGroupFn, create_group_steps: CreateGroupStepsFn, group_chat_details: GroupChatDetailsFn, add_group_member_action: AddGroupMemberActionFn, group_name: str):
    room = cast("MultiChatRoom | None", next((r for r in ChatRoom.chatroom if isinstance(r, MultiChatRoom) and r.group_name == group_name), None))

    if room:
        add_group_member_action(userDetails, user, groups_list, room, group_name, user.username, room.addUserToRoom, lambda name: f"\n@{name} not a user, can't add to group!")
    else:
        choice = int(input(f"\nGroup chat with {group_name} does not exist!\n\n1. Create group chat {group_name}\n2. View group list\n3. Go home\n\n"))

        group_not_exists(choice, user, userDetails, create_group, create_group_steps, group_chat_details, add_group_member_action, group_name)

def no_group_list_exists(choice: int, user: User, userDetails: UserDetailsFn, create_group: CreateGroupFn, create_group_steps: CreateGroupStepsFn, group_chat_details: GroupChatDetailsFn, add_group_member_action: AddGroupMemberActionFn):
    match choice:
        case 1:
            create_group(user, userDetails)
        case 2:
            group_name = input("\nEnter group chat name: ")

            send_group_request(user, userDetails, create_group, create_group_steps, group_chat_details, add_group_member_action, group_name)
        case 3:
            userDetails(user)
        case _:
            choice = int(input(f"{choice} not part of the options available\n\n1. Create group chat\n2. Send group chat request\n3. Go home\n\n"))

            no_group_list_exists(choice, user, userDetails, create_group, create_group_steps, group_chat_details, add_group_member_action)

def group_not_list(choice: int, user: User, userDetails: UserDetailsFn, create_group: CreateGroupFn, create_group_steps: CreateGroupStepsFn, group_chat_details: GroupChatDetailsFn, add_group_member_action: AddGroupMemberActionFn, group_name: str):
    match choice:
        case 1:
            create_group_steps(user, userDetails, group_name)
        case 2:
            send_group_request(user, userDetails, create_group, create_group_steps, group_chat_details, add_group_member_action, group_name)
        case 3:
            userDetails(user)
        case _:
            choice = int(input(f"{choice} not part of the options available!\n\n1. Create group chat {group_name}\n2. Send group chat request for {group_name}\n3. Go home\n\n"))

            group_not_list(choice, user, userDetails, create_group, create_group_steps, group_chat_details, add_group_member_action, group_name)

def group_list_exists(choice: int, user: User, userDetails: UserDetailsFn, create_group: CreateGroupFn, create_group_steps: CreateGroupStepsFn, group_chat_details: GroupChatDetailsFn, add_group_member_action: AddGroupMemberActionFn):
    match choice:
        case 1:
            group_name = input("\nEnter group chat name: ")

            if group_name in user.groups:
                room = cast("MultiChatRoom | None", next((r for r in ChatRoom.chatroom if isinstance(r, MultiChatRoom) and r.group_name == group_name), None))

                group_chat_details(userDetails, user, groups_list, room, group_name)
            else:
                choice = int(input(f"\nGroup chat with {group_name} does not exist in your list!\n\n1. Create group chat {group_name}\n2. Send group chat request for {group_name}\n3. Go home\n\n"))

                group_not_list(choice, user, userDetails, create_group, create_group_steps, group_chat_details, add_group_member_action, group_name)
        case 2:
            create_group(user, userDetails)
        case 3:
            userDetails(user)
        case _:
            choice = int(input(f"{choice} not part of the options available\n\n1. Visit group chat\n2. Create group chat\n3. Go home\n\n"))

            group_list_exists(choice, user, userDetails, create_group, create_group_steps, group_chat_details, add_group_member_action)

def groups_list(user: User, userDetails: UserDetailsFn, create_group: CreateGroupFn, create_group_steps: CreateGroupStepsFn, group_chat_details: GroupChatDetailsFn, add_group_member_action: AddGroupMemberActionFn):
    if user.groups:
        print("\nGroups:")

        for i, g in enumerate(user.groups, start=1):
            print(f"{i}. {g}")

        choice = int(input("\n1. Visit group chat\n2. Create group chat\n3. Go home\n\n"))

        group_list_exists(choice, user, userDetails, create_group, create_group_steps, group_chat_details, add_group_member_action)
    else:
        choice = int(input("\nYou're currently not in a group\n\n1. Create group chat\n2. Send group chat request\n3. Go home\n\n"))

        no_group_list_exists(choice, user, userDetails, create_group, create_group_steps, group_chat_details, add_group_member_action)