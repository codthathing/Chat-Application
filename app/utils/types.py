from typing import Callable, TypeAlias
from  models.User import User
from models.ChatRoom import MultiChatRoom

UserDetailsFn: TypeAlias = Callable[..., None]
AddFriendFn: TypeAlias = Callable[..., None]
FriendChatOptionsFn: TypeAlias = Callable[..., None]
FriendAddConditionFn: TypeAlias = Callable[..., None]
FriendsListFn: TypeAlias = Callable[..., None]
GroupChatDetailsFn: TypeAlias = Callable[..., None]
CreateGroupFn: TypeAlias = Callable[..., None]
AddGroupMemberActionFn: TypeAlias = Callable[..., None]
CreateGroupStepsFn: TypeAlias = Callable[..., None]
GroupsListFn: TypeAlias = Callable[..., None]

# UserDetailsFn: TypeAlias = Callable[[User], None]
# AddFriendFn: TypeAlias = Callable[[User, "UserDetailsFn", str], None]
# FriendChatOptionsFn: TypeAlias = Callable[..., None]
# FriendAddConditionFn: TypeAlias = Callable[["UserDetailsFn", "FriendsListFn", User, str], None]
# FriendsListFn: TypeAlias = Callable[..., None]
# GroupChatDetailsFn: TypeAlias = Callable[["UserDetailsFn", User, MultiChatRoom, str], None]
# CreateGroupFn: TypeAlias = Callable[[User, "UserDetailsFn"], None]
# AddGroupMemberActionFn: TypeAlias = Callable[["UserDetailsFn", User, MultiChatRoom, str, Callable[[User, User], str], Callable[[str], str]], None]
# CreateGroupStepsFn: TypeAlias = Callable[..., None]
# GroupsListFn: TypeAlias = Callable[..., None]