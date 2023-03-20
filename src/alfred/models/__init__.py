from alfred.dao.interface import BaseModel
from typing import List, Type


class ModelRegistry:

    @staticmethod
    def find_all() -> List[Type[BaseModel]]:
        import pkgutil
        import inspect
        import importlib

        module = importlib.import_module(__name__)  # Import current module
        return [
            cls_ref
            for submodule_info in pkgutil.iter_modules(module.__path__)
            for cls_name, cls_ref in inspect.getmembers(
                importlib.import_module(".".join([__name__, submodule_info.name])),
                inspect.isclass
            )
            if issubclass(cls_ref, BaseModel) and cls_ref != BaseModel
        ]
