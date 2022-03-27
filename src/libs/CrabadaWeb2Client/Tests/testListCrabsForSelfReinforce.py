from src.common.config import users
from src.libs.CrabadaWeb2Client.CrabadaWeb2Client import CrabadaWeb2Client
from pprint import pprint

# VARS
client = CrabadaWeb2Client()
userAddress = users[0]["address"]

# TEST FUNCTIONS
def testListCrabsForSelfReinforce() -> None:
    pprint(client.listCrabsForSelfReinforce(userAddress))

# EXECUTE
print(">>> AVAILABLE CRABS FOR SELF REINFORCE")
testListCrabsForSelfReinforce()
