from typing import cast
from eth_typing import Address
from hexbytes import HexBytes
from web3.types import TxParams, Wei
from src.libs.Web3Client.Web3Client import Web3Client
from src.libs.Web3Client.AvalancheCWeb3Client import AvalancheCWeb3Client
from eth_typing.encoding import HexStr
import os
from time import sleep

class CrabadaWeb3Client(AvalancheCWeb3Client):
    """
    Interact with a smart contract of the game Crabada

    The contract resides on the Avalanche blockchain; here's
    the URL on Snowtrace:
    https://snowtrace.io/address/0x82a85407bd612f52577909f4a58bfc6873f14da8#tokentxns
    """

    contractAddress = cast(Address, "0x82a85407bd612f52577909f4a58bfc6873f14da8")
    abiDir = os.path.dirname(os.path.realpath(__file__)) + "/contracts"
    abi = Web3Client.getContractAbiFromFile(abiDir + "/IdleGameAbi.json")

    def __init__(
        self,
        nodeUri: str,
        privateKey: str = None,
        maxPriorityFeePerGasInGwei: float = 1,
        upperLimitForBaseFeeInGwei: float = float("inf"),
    ) -> None:
        super().__init__(
            nodeUri=nodeUri,
            privateKey=privateKey,
            maxPriorityFeePerGasInGwei=maxPriorityFeePerGasInGwei,
            upperLimitForBaseFeeInGwei=upperLimitForBaseFeeInGwei,
            contractAddress=self.contractAddress,
            abi=self.abi,
        )

    def startGame(self, teamId: int) -> HexStr:
        """
        Send crabs to mine
        """
        tx: TxParams = self.buildContractTransaction(
            self.contract.functions.startGame(teamId),
        )
        return self.signAndSendTransaction(tx)

    def attack(
        self, gameId: int, teamId: int, expiredTime: int, certificate: HexBytes
    ) -> HexStr:
        """
        Attack an open mine
        """
        tx: TxParams = self.buildContractTransaction(
            self.contract.functions.attack(gameId, teamId, expiredTime, certificate),
        )
        return self.signAndSendTransaction(tx)

    def closeGame(self, gameId: int) -> HexStr:
        """
        Close mining game, claim reward & send crabs back home
        """
        contract_fn =  self.contract.functions.closeGame(gameId)
        contract_fn.call({'from': self.userAddress})

        tx: TxParams = self.buildContractTransaction(contract_fn)
        return self.signAndSendTransaction(tx)

    def settleGame(self, gameId: int) -> HexStr:
        """
        Close looting game, claim reward & send crabs back home
        """
        contract_fn = self.contract.functions.settleGame(gameId)
        contract_fn.call({'from': self.userAddress})

        tx: TxParams = self.buildContractTransaction(contract_fn)
        return self.signAndSendTransaction(tx)

    def reinforceDefense(self, gameId: int, crabadaId: int, borrowPrice: Wei) -> HexStr:
        """
        Hire a crab from the tavern to reinforce the mining team; the
        price must be expressed in Wei (1 TUS = 10^18 Wei)
        """

        contract_fn = self.contract.functions.reinforceDefense(gameId, crabadaId, borrowPrice)
        contract_fn.call({'from': self.userAddress})
        sleep(2)
        contract_fn.call({'from': self.userAddress})

        tx: TxParams = self.buildContractTransaction(contract_fn)
        return self.signAndSendTransaction(tx)

    def reinforceAttack(self, gameId: int, crabadaId: int, borrowPrice: Wei) -> HexStr:
        """
        Hire a crab from the tavern to reinforce the looting team;
        the price must be expressed in Wei (1 TUS = 10^18 Wei)
        """

        contract_fn = self.contract.functions.reinforceAttack(gameId, crabadaId, borrowPrice)
        contract_fn.call({'from': self.userAddress})
        sleep(2)
        contract_fn.call({'from': self.userAddress})

        tx: TxParams = self.buildContractTransaction(contract_fn)
        return self.signAndSendTransaction(tx)
