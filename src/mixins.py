#! python3

""" Collection of mixins for additional functionality """

# Built-in libraries
import math
import json

from pathlib import Path
from typing import List, Dict, Union, Any, NewType
from copy import deepcopy
from functools import lru_cache
from abc import ABCMeta, abstractmethod

# 3rd-party libraries
import toml

# Local libraries
from settings import *


class DataFileMixin(metaclass=ABCMeta):
    """ Contains methods for getting game data from files """

    @staticmethod
    @lru_cache(maxsize=128, typed=True)
    def _get_by_ID(ID: int, obj_type: str, file: str, file_format: str=DATA_FORMAT) -> Dict:
        """ 'Low-level' access to filedata """
        with open(file) as f:
            if file_format == "json":
                data = json.load(f, parse_int=int, parse_float=float)
            elif file_format == "toml":
                data = toml.load(f)
            else:
                raise NotImplementedError(f"Missing support for opening files of type: {file_format}")
        return data[obj_type][str(ID)]

    def get_item_by_ID(self, ID: int, file: str=ITEM_FILE) -> Dict:
        """ Returns a dictionary representation of a given item ID """
        return self._get_by_ID(ID, 'items', file)

    def get_enemy_by_ID(self, ID: int, file: str=ENEMY_FILE) -> Dict:
        """ Returns a dictionary representation of a given enemy ID """
        return self._get_by_ID(ID, 'enemies', file)

    def get_npc_by_ID(self, ID: int, file: str=NPC_FILE) -> Dict:
        """ Returns a dictionary representation of a given NPC ID """
        return self._get_by_ID(ID, 'NPCs', file)

    def get_entity_by_ID(self, ID: int, file: str=ENTITY_FILE) -> Dict:
        """ Returns a dictionary representation of a given entity ID """
        return self._get_by_ID(ID, 'entities', file)


class ReprMixin(metaclass=ABCMeta):
    """ Automatically generates a __repr__-method for any class """

    def __repr__(self):
        """ Automatically generated __repr__-method """

        attributes = [f"{key}={value}" if type(value) != str
                     else f'{key}="{value}"'
                     for key, value in vars(self).items()]
        v_string = ", ".join(attributes)
        class_name = self.__class__.__name__
        return f"{class_name}({v_string})"


class LevelMixin(metaclass=ABCMeta):
    """ Gives standard level-up mechanics for the child class """
    def __init__(self, **kwargs):
        """
        Initialises the child class' attributes

        Accepted kwargs:
        - level: combat level, defaults to 1
        - max_level: sets a level cap for the object, defaults to None
        - exp: current experience points, defaults to 0
        - exponent: modifies the XP curve required to level-up, defaults to 1.6
        - base_exp: sets the EXP required to reach level 2, defaults to 85
        """
        #super(LevelMixin, self).__init__()
        self.level: int = int(kwargs.get("level", 1))
        self.experience: int = int(kwargs.get("exp", 0))
        self.exponent: float = float(kwargs.get("exponent", 1.6))
        self._base_exp: int = int(kwargs.get("base_exp", 85))
        self.max_level: Union[int, None] = kwargs.get("max_level", None)

    @property
    def next_level(self) -> int:
        """
        Returns the amount of EXP needed for the next level.

        No built-in level cap.
        """

        return math.floor(self._base_exp * (self.level**self.exponent))

    def level_up(self, print_exp: bool=False) -> Union[str, None]:
        """
        Checks if object has acquired enough EXP to level up.

        If it has, levelup() will increment the player's level and run again until
        the object's EXP isn't enough for the next level, or until max_level is reached
        (unless max_level is None).

        Ends by printing the amount of EXP required to reach the next level.
        If max_level has been set and level >= max_level, nothing is printed.

        This method has an optional argument, print_exp, which will determine if
        the EXP is printed in the end. By default, it will be printed if a level is gained.
        By changing it to True, the EXP required is printed regardless.
        By changing it to None, the EXP is never printed.
        """

        results = []
        gained_levels = 0

        while self.next_level <= self.experience:
            if self.level == self.max_level:
                break

            if self.max_level is None or self.level < self.max_level:
                self.level += 1
                gained_levels += 1
                if print_exp is not None:
                    print_exp = True

        if gained_levels == 1:
            results.append(f"Congratulations! You've levelled up; your new level is {self.level}")
        elif gained_levels > 1:
            results.append(f"Congratulations! You levelled up {gained_levels} times in one go. Your new level is {self.level}")

        if print_exp and (self.max_level is None or self.level < self.max_level):
            results.append(f"EXP required for next level: {int(self.next_level-self.experience)}")

        if print_exp:
            results.append(f"Current EXP: {self.experience}")

        formatted_results = "\n".join(results)
        return formatted_results

    def give_exp(self, amount: int, check_level_up=True, print_exp=False) -> Union[str, None]:
        """
        Give the object experience points.

        Automatically checks for level-up unless set to False.
        """
        self.experience += amount
        if check_level_up:
            return self.level_up(print_exp)
        return None

class SpritesMixin(metaclass=ABCMeta):
    """
    Contains methods for loading sprites for game objects

    Future: Implement other general sprite functionality
    """

    @staticmethod
    def __load_sprites(type: str, obj: str) -> List: #TODO: Fill in the sprite object type
        path = Path(__file__).parent / "img" / type / obj
        sprites = []
        for sprite in path.resolve().glob('**/*'):
            #TODO: Implement file loading as file objects
            sprites.append(str(sprite))
        return sprites

    def load_char_sprites(self, name: str):
        return self.__load_sprites('chars', name.lower())

    def load_item_sprites(self, ID: int):
        return self.__load_sprites('items', str(ID))
