import time

import streamlit as st

from alfred.models.user import User
from alfred.utils.pwd import password_hash
from alfred.utils.json_web_token import JsonWebToken
from alfred.frontend.interface import ViewInterface
from alfred.settings import get_logger

logger = get_logger(name=__name__)


class StartSession(ViewInterface):
    login_required = False
    disable_user_info = False
    hidden_if_session_active = True
    order_reference = 2

    @property
    def alias(self) -> str:
        return "Start Session"

    def run(self):
        with st.form("session"):
            user_email = st.text_input(label="Email")
            user_pwd = st.text_input(label="Password", type="password")
            submitted = st.form_submit_button("Start Session")

        if not submitted:
            return None

        try:
            user = User.get(email=user_email)
            pwd_hash = password_hash(pwd=user_pwd, salt=user.password_salt)
            if user.password_hash != pwd_hash:
                raise ValueError
        except Exception as e:
            logger.error(e)
            return st.error("User email or pwd is wrong.")

        jwt = JsonWebToken.auto_configure(verify_exp=True)
        st.session_state["token"] = jwt.encode(payload=user.session())
        st.success(f"Welcome {user.name}!")
        with st.spinner("Logging into our system..."):
            time.sleep(1)
        st.experimental_rerun()
