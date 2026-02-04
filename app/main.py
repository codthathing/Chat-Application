from models.User import User
from models.ChatRoom import MultiUser, DualUser
from typing import cast

segun = User("@pheezy", "akinwunmiolusegun277@gmail.com", "#Pheezy123")
bolu = User("@tife", "boluwatifeakinwunmi@gmail.com", "tife123")
abiodun = User("@abiodun", "akinwunmi.abiodun1965@gmail.com", "abiodun1965")
folabi = User("@folabi", "afolabi.creator@gmail.com", "#Pheezy123")
print(User.usernames)

group: MultiUser = cast(MultiUser, bolu.createChatRoom("multi", [segun, folabi]))
group.addRoomAdmin(bolu, segun)
print(group)

mutual: DualUser = cast(DualUser, folabi.createChatRoom("dual", abiodun))
print(mutual)