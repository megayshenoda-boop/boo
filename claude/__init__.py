"""
IGG Conquerors Bot Package
===========================
Clean, modular bot for IGG Conquerors (الفاتحون).
"""
from .config import IGG_ID, GAME_ID, WORLD_ID
from .codec import CMsgCodec, extract_server_key_from_0x0038
from .game_server import GameConnection
from .commands import CommandEngine
from .bot import ConquerorsBot

__all__ = [
    'ConquerorsBot', 'GameConnection', 'CommandEngine',
    'CMsgCodec', 'extract_server_key_from_0x0038',
    'IGG_ID', 'GAME_ID', 'WORLD_ID',
]
