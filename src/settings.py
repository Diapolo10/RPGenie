import os

DATA_FILE = "items.toml" #DEPRECATED
DATA_DIR = "data"
DATA_FORMAT = "toml"

ITEM_FILE = os.path.join(DATA_DIR, f"items.{DATA_FORMAT}")
ENTITY_FILE = os.path.join(DATA_DIR, f"entities.{DATA_FORMAT}")
ENEMY_FILE = os.path.join(DATA_DIR, f"enemies.{DATA_FORMAT}")
NPC_FILE = os.path.join(DATA_DIR, f"npcs.{DATA_FORMAT}")
QUEST_FILE = os.path.join(DATA_DIR, f"quests.{DATA_FORMAT}")
OBJECT_FILE = os.path.join(DATA_DIR, f"objects.{DATA_FORMAT}")
