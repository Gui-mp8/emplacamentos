from abc import ABC, abstractmethod
from typing import List, Dict, Any

class SavingFiles(ABC):

    @abstractmethod
    def folder_creation(self):
        pass

    @abstractmethod
    def writing_data(self, data: List[Dict[str, Any]], file_name: str) -> None:
        pass
