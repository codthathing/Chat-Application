from models.User import User
from models.ChatRoom import MultiUser, DualUser

segun = User("@pheezy", "akinwunmiolusegun277@gmail.com", "#Pheezy123")
bolu = User("@tife", "boluwatifeakinwunmi@gmail.com", "tife123")
abiodun = User("@abiodun", "akinwunmi.abiodun1965@gmail.com", "abiodun1965")
folabi = User("@folabi", "afolabi.creator@gmail.com", "#Pheezy123")
print(User.usernames)

group: MultiUser = bolu.createMultiUserRoom([segun, folabi])
group.addRoomAdmin(bolu, segun)
print(group)

mutual: DualUser = folabi.createDualUserRoom(abiodun)
print(mutual)