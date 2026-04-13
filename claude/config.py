"""
IGG Conquerors Bot - Configuration
===================================
All constants, credentials, and server addresses.
Credentials can be overridden via environment variables.
"""
import os

# Account
IGG_ID = int(os.environ.get("IGG_ID", "577962733"))
GAME_ID = os.environ.get("GAME_ID", "1057029902")
GAME_ID_HEX = 0x3F00FF0E
WORLD_ID = int(os.environ.get("WORLD_ID", "211"))

# Credentials (MUST be set via environment variables!)
EMAIL = os.environ.get("IGG_EMAIL", "")
PASSWORD = os.environ.get("IGG_PASSWORD", "")
STORED_ACCESS_KEY = os.environ.get("IGG_ACCESS_KEY", "")

# Network
GATEWAY_IP = "54.93.167.80"
GATEWAY_PORT = 5997
HEARTBEAT_INTERVAL = 15.0

# Crypto
HMAC_KEY = "07Z8D2AoYFGGivw40fEOj9swnpyF7Pw3ilKpVKnJ"
CQ_XOR_KEY = ("CQ_secret" * 4)[:32]  # "CQ_secretCQ_secretCQ_secretCQ_se"

# User Agent
USER_AGENT = f"{GAME_ID}/6.3.0 Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G9880 Build/N2G47H)"

# ADB (for emulator key extraction)
ADB_PATH = os.environ.get("ADB_PATH", r"D:\Program Files\Microvirt\MEmu\adb.exe")
ADB_DEVICE = os.environ.get("ADB_DEVICE", "127.0.0.1:21503")
