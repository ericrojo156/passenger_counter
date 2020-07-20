from abc import ABC, abstractmethod
import typing

class ConfigIO(ABC):
    @abstractmethod
    def save_config_json(self, config_dict: str):
        pass
    @abstractmethod
    def load_config_json(self) -> str:
        pass
    @abstractmethod
    def select_default_source(self):
        pass