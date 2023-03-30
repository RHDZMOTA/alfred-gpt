import datetime as dt
from typing import Optional
from types import TracebackType


from alfred.models.user import User
from alfred.settings import get_logger
from alfred.frontend.functions import get_user
from alfred.utils.string_ops import camel_to_snake


logger = get_logger(name=__name__)


class ViewInterface:
    order_reference: int
    login_required: bool = False
    disable_user_info: bool = False
    hidden_if_session_active: bool = False
    _instance = None

    def __init__(self):
        raise ValueError

    def __new__(cls, *args, **kwargs):
        cls.view_timestamp = dt.datetime.utcnow().isoformat()
        return super().__new__(cls)

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = cls.__new__(cls)
        return cls._instance

    def __enter__(self):
        user_instance = self.user
        if self.login_required and not user_instance:
            return None
        # Should we disable the user info?
        if self.disable_user_info:
            if self.hidden_if_session_active and user_instance:
                return None
            return self
        # Should we display the user info?
        if user_instance:
            import streamlit as st
            st.info(f"Logged as {user_instance.name}")
        if self.hidden_if_session_active and user_instance:
            return None
        return self

    def __exit__(
            self,
            exc_type: Optional[type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType],
    ):
        ok = exc_val is None
        logger.info(
            "View (%s) execution: %s",
            self.alias,
            "successful" if ok else "failure"
        )

    @property
    def alias(self) -> str:
        name = getattr(self, "__name__")  # Why not self.__name__? Because mypy...
        # References:
        # - https://github.com/python/cpython/issues/88690
        # - https://github.com/python/mypy/issues/10403
        # - https://github.com/python/mypy/issues/12795
        # - https://docs.python.org/3/library/stdtypes.html#definition.__name__
        return camel_to_snake(name)

    @property
    def user(self) -> Optional[User]:
        return get_user()

    def run(self):
        raise NotImplementedError
