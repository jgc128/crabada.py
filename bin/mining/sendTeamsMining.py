#!/usr/bin/env python3
"""
Crabada script to send mining all available teams for
the given user.

Usage:
    python3 -m bin.mining.sendTeamsMining <userAddress>

Author:
    @coccoinomane (Twitter)
"""
from pathlib import Path

from src.bot.mining.sendTeamsMining import sendTeamsMining
from src.helpers.general import secondOrNone
from src.models.User import User
from src.common.logger import logger
from sys import argv, exit

userAddress = secondOrNone(argv)

no_mine_path = Path(__file__).parent.parent.joinpath(f'.no_mine_{userAddress}')
if no_mine_path.exists():
    logger.error(f"No mine: {userAddress}")
    exit(1)

if not userAddress:
    logger.error("Specify a user address")
    exit(1)

nSent = sendTeamsMining(User(userAddress))
