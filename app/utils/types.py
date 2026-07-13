from typing import Callable, TypeAlias

UserDetailsFn: TypeAlias = Callable[..., None]
AddFriendFn: TypeAlias = Callable[..., None]
FriendChatOptionsFn: TypeAlias = Callable[..., None]
FriendAddConditionFn: TypeAlias = Callable[..., None]
FriendsListFn: TypeAlias = Callable[..., None]
GroupChatDetailsFn: TypeAlias = Callable[..., None]
CreateGroupFn: TypeAlias = Callable[..., None]
AddGroupMemberActionFn: TypeAlias = Callable[..., None]