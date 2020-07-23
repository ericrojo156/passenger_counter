from abc import ABC, abstractmethod
import typing

class ConfigIO(ABC):
    @abstractmethod
    def save_config_json(self, config_json: str):
        pass
    @abstractmethod
    def load_config_json(self) -> str:
        pass
    @abstractmethod
    def select_default_source(self, should_select=True):
        pass