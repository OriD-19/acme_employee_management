import os
import json
from typing import TypedDict, cast

class DefinedConfigurationProperties(TypedDict, total=False):
    salaryBonusPercentage: float
    minHoursForHourlyBonus: int


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Config(metaclass=SingletonMeta):
    def __init__(self, path="config.json"):
        self.path = path
        self.config: DefinedConfigurationProperties = self._load_config()

    def _load_config(self):
        if not os.path.exists(self.path):
            print(f"[WARN] Config file '{self.path}' not found. Using defaults.")
            # default values for the system
            return {
                "salaryBonusPercentage": 0.10,
                "minHoursForHourlyBonus": 160
            }

        with open(self.path, "r", encoding="utf-8") as f:
            return cast(DefinedConfigurationProperties, json.load(f))

    def get(self, key: str, default=None):
        return self.config.get(key, default)

    def require(self, key: str):
        try:
            return self.config[key]
        except KeyError:
            raise KeyError(f"need the key {key} to be defined in the configuration file")


config = Config()
