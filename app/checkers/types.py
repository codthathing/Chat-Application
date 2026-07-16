from typing import TypeAlias, Callable
from models.User import User
from models.ChatRoom import DualChatRoom, MultiChatRoom

UserDetailsFn: TypeAlias = Callable[[User], None]

AddFriendFn: TypeAlias = Callable[[User, UserDetailsFn, "FriendsListFn"], None]

FriendChatOptionsFn: TypeAlias = Callable[[UserDetailsFn, "FriendsListFn", int, User, DualChatRoom], None]

FriendAddConditionFn: TypeAlias = Callable[[UserDetailsFn, "FriendsListFn", User, str], None]

FriendsListFn: TypeAlias = Callable[[User, UserDetailsFn, AddFriendFn, FriendChatOptionsFn, FriendAddConditionFn], None]

GroupChatDetailsFn: TypeAlias = Callable[[UserDetailsFn, User, FriendAddConditionFn, FriendsListFn, "GroupsListFn", MultiChatRoom, str], None]

CreateGroupFn: TypeAlias = Callable[[User, UserDetailsFn, FriendAddConditionFn, FriendsListFn, "GroupsListFn"], None]

AddGroupMemberActionFn: TypeAlias = Callable[[UserDetailsFn, User, FriendAddConditionFn, FriendsListFn, "GroupsListFn", MultiChatRoom, str, str, Callable[[User, User], str], Callable[[str], str], bool], None]

CreateGroupStepsFn: TypeAlias = Callable[[User, UserDetailsFn, FriendAddConditionFn, FriendsListFn, "GroupsListFn", str], None]

GroupsListFn: TypeAlias = Callable[[User, UserDetailsFn, FriendAddConditionFn, FriendsListFn, CreateGroupFn, CreateGroupStepsFn, GroupChatDetailsFn, AddGroupMemberActionFn], None]