import datetime as dt
from typing import Dict, Optional, Callable

from alfred.frontend.interface import ViewInterface
from alfred.utils.string_ops import camel_to_snake


class ViewController:
    views: Dict[str, Callable]
    _created_at: dt.datetime
    _instance = None

    def __init__(self):
        raise ValueError("Call the 'instance' method instead.")

    def __new__(cls, *args, **kwargs):
        import pkgutil
        import inspect
        import importlib

        module = importlib.import_module("alfred.frontend.views")  # Import current module
        cls.views: Dict[str, ViewInterface] = {
            camel_to_snake(cls_name): cls_ref
            for submodule_info in pkgutil.iter_modules(module.__path__)
            for cls_name, cls_ref in inspect.getmembers(
                importlib.import_module(".".join([module.__name__, submodule_info.name])),
                inspect.isclass
            )
            if issubclass(cls_ref, ViewInterface) and cls_ref != ViewInterface
        }
        cls._created_at = dt.datetime.utcnow()
        return super().__new__(cls)

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = cls.__new__(cls)
        return cls._instance

    def run(self, view_name: Optional[str] = None,  **kwargs):
        import streamlit as st

        # Query params
        query_params = st.experimental_get_query_params()

        # Default values
        view_name, *_ = query_params.get("view", [view_name or "about"])
        views = {
            view_name: view_ref.instance()
            for view_name, view_ref in self.views.items()
        }

        # Define the sidebar
        view_selection, _ = st.sidebar.radio(
            key="views_sidebar",
            label="Alfred Options",
            options=sorted(
                [
                    (view_name, view_instance.order_reference)
                    for view_name, view_instance in views.items()
                ],
                key=lambda view_info: view_info[-1],
                reverse=False,
            ),
            format_func=lambda view_info: views[view_info[0]].alias,
        )

        # Update query params to the corresponding value
        st.experimental_set_query_params(view=view_selection)
        views[view_selection].run(**kwargs)
