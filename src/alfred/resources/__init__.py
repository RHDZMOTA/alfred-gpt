import os
from typing import List


class ResourceManager:

    @staticmethod
    def get_basepath() -> str:
        return os.path.dirname(__file__)

    @classmethod
    def resources(cls) -> List[str]:
        return os.listdir(cls.get_basepath())

    @classmethod
    def get(cls, name: str) -> str:
        if name not in cls.resources():
            raise ValueError("Resource not found: %s", name)
        with open(os.path.join(cls.get_basepath(), name), "r") as file:
            return file.read()
