
from typing import Any, List, Tuple
from eth_typing import Address
import requests

from src.libs.CrabadaWeb2Client.types import CrabForLending, Game, Team

class CrabadaWeb2Client:
    """Access the HTTP endpoints of the Crabada P2E game.
    
    All endpoints have a 'raw' parameter that you can set to true
    in order to get the full JSON response. By default it is false,
    which means you only get the data contained in the response (a
    list for list endpoints, a dict for specific endpoints)"""

    baseUri = 'https://idle-api.crabada.com/public/idle'

    def getMine(self, mineId: int, params: dict[str, Any] = {}) -> Game:
        """Get information from the given mine"""
        res = self.getMine_Raw(mineId, params)
        return res['result']
    
    def getMine_Raw(self, mineId: int, params: dict[str, Any] = {}) -> Any:
        url = self.baseUri + '/mine/' + str(mineId)
        return requests.request("GET", url, params=params).json()

    def listMines(self, params: dict[str, Any] = {}) -> List[Game]:
        """Get all mines.
        
        If you want only the open mines, pass status=open in the params.
        If you want only a certain user's mines, use the user_address param.
        """
        res = self.listMines_Raw(params)
        try:
            return res['result']['data'] or []
        except:
            return []

    def listMines_Raw(self, params: dict[str, Any] = {}) -> Any:
        url = self.baseUri + '/mines'
        defaultParams = {
            "limit": 5,
            "page": 1,
        }
        actualParams = defaultParams | params
        return requests.request("GET", url, params=actualParams).json()

    def listTeams(self, userAddress: Address, params: dict[str, Any] = {}) -> List[Team]:
        """Get all teams of a given user address.
        
        If you want only the available teams, pass is_team_available=1
        in the params.
        It is currently not possible to list all users' teams, you can
        only see the teams of a specific user.
        """
        res = self.listTeams_Raw(userAddress, params)
        try:
            return res['result']['data'] or []
        except:
            return []

    def listTeams_Raw(self, userAddress: Address, params: dict[str, Any] = {}) -> Any:
        url = self.baseUri + '/teams'
        defaultParams = {
            "limit": 5,
            "page": 1,
        }
        actualParams = defaultParams | params
        actualParams['user_address'] = userAddress
        return requests.request("GET", url, params=actualParams).json()

    def listCrabsForLending(self, params: dict[str, Any] = {}) -> List[CrabForLending]:
        """Get all crabs available for lending as reinforcements; you can use
        sortBy and sort parameters, default is orderBy": 'price' and
        "order": 'asc'"""
        res = self.listCrabsForLending_Raw(params)
        try:
            return res['result']['data'] or []
        except:
            return []

    def listCrabsForLending_Raw(self, params: dict[str, Any] = {}) -> Any:
        url = self.baseUri + '/crabadas/lending'
        defaultParams = {
            "limit": 10,
            "page": 1,
            "orderBy": 'price',
            "order": 'asc',
        }
        actualParams = defaultParams | params
        return requests.request("GET", url, params=actualParams).json() # type: ignore