from pathlib import Path

# TODO: Deprecated; define a class and define settings as properties to evaluate them on-demand

DATA_DIR = Path(__file__).parent / "data"
DATA_FORMAT = "json"
ITEM_MAX_COUNT = 10**5 #Used to change item description

ITEM_FILE = str(DATA_DIR / f"items.{DATA_FORMAT}")
ENTITY_FILE = str(DATA_DIR / f"entities.{DATA_FORMAT}")
ENEMY_FILE = str(DATA_DIR / f"enemies.{DATA_FORMAT}")
NPC_FILE = str(DATA_DIR / f"npcs.{DATA_FORMAT}")
QUEST_FILE = str(DATA_DIR / f"quests.{DATA_FORMAT}")
OBJECT_FILE = str(DATA_DIR / f"objects.{DATA_FORMAT}")

__all__ = ('settings',)


class GlobalSettings:

    def __init__(self, data_format='json', stack_examine_limit=10**5):
        self.data_dir = Path(__file__).parent / 'data'
        self.data_format = data_format
        self.stack_examine_limit = stack_examine_limit

    @property
    def item_file(self):
        return str(self.data_dir / f'items.{data_format}')

    @property
    def entity_file(self):
        return str(self.data_dir / f"entities.{DATA_FORMAT}")

    @property
    def enemy_file(self):
        return str(self.data_dir / f"enemies.{DATA_FORMAT}")

    @property
    def npc_file(self):
        return str(self.data_dir / f"npcs.{DATA_FORMAT}")

    @property
    def quest_file(self):
        return str(self.data_dir / f"quests.{DATA_FORMAT}")

    @property
    def object_file(self):
        return str(self.data_dir / f"quests.{DATA_FORMAT}")


settings = GlobalSettings()
