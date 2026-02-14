from models.User import User
from models.ChatRoom import MultiUser, DualUser
from schemas.UsersRoomSchema import UsersRoomSchema

chatSchema = UsersRoomSchema()

segun: User = chatSchema.createUser("@pheezy", "akinwunmiolusegun277@gmail.com")
bolu: User = chatSchema.createUser("@tife", "boluwatifeakinwunmi@gmail.com")
abiodun: User = chatSchema.createUser("@abiodun", "akinwunmi.abiodun1965@gmail.com")
folabi: User = chatSchema.createUser("@folabi", "afolabi.creator@gmail.com")

group: MultiUser = bolu.createMultiUserRoom([segun])
group.addRoomAdmin(bolu, segun)
group.addUserToRoom(segun, folabi)

mutual: DualUser = folabi.createDualUserRoom(abiodun)
mutual.enterChatToRoom(folabi, "Hello world")

chatSchema.updateUsername(folabi, "@fola_creator")
chatSchema.updateEmail(bolu, "boluwatifesther@gmail.com")

print(repr(chatSchema))