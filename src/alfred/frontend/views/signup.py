import streamlit as st

from alfred.models.user import User
from alfred.frontend.interface import ViewInterface
from alfred.settings import get_logger

logger = get_logger(name=__name__)


class Signup(ViewInterface):
    login_required = False
    disable_user_info = False
    hidden_if_session_active = True
    order_reference = 1

    @property
    def alias(self) -> str:
        return "Signup"

    def run(self):
        with st.form("signup"):
            user_name = st.text_input(label="User Name")
            user_email = st.text_input(label="Email")
            user_pwd = st.text_input(label="Password", type="password")
            activation_code = st.text_input(label="Activation Code", type="password")
            submitted = st.form_submit_button("Create")

        if not submitted:
            return None
        with st.spinner("Creating your user..."):
            try:
                user = User.create(
                    activation_code=activation_code,
                    password=user_pwd,
                    name=user_name,
                    email=user_email,
                )
            except Exception:
                st.warning(f"User {repr(user_name)} was not created")
                return
        # TODO: Add confirmation email flow
        st.success(f"User {repr(user.name)} successfully created! ")
        st.markdown("Check your email to verify your user.")
