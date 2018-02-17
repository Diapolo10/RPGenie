from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
DATA_FORMAT = "json"
ITEM_MAX_COUNT = 10**5 #Used to change item description

ITEM_FILE = str(DATA_DIR / f"items.{DATA_FORMAT}")
ENTITY_FILE = str(DATA_DIR / f"entities.{DATA_FORMAT}")
ENEMY_FILE = str(DATA_DIR / f"enemies.{DATA_FORMAT}")
NPC_FILE = str(DATA_DIR / f"npcs.{DATA_FORMAT}")
QUEST_FILE = str(DATA_DIR / f"quests.{DATA_FORMAT}")
OBJECT_FILE = str(DATA_DIR / f"objects.{DATA_FORMAT}")
