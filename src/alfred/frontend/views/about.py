import textwrap
from typing import Optional

import streamlit as st

from alfred.models.user import User
from alfred.frontend.functions import get_user
from alfred.frontend.interface import ViewInterface


class About(ViewInterface):
    login_required = False
    disable_user_info = True
    hidden_if_session_active = False
    order_reference = 0

    @property
    def alias(self) -> str:
        return "About Alfred"

    @property
    def user(self) -> Optional[User]:
        return get_user()

    def run(self):
        st.title("Introducing Alfred")
        st.subheader("Your personal intelligent assistant.")

        st.markdown(
            textwrap.dedent(
                """
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi eu ultricies purus.
                Cras quis lacus turpis. Nam sit amet aliquet mi. Duis lacinia, justo in faucibus tristique,
                leo dui tempus mauris, eget aliquam mauris erat ac leo. Nam urna odio, scelerisque et nisi sit amet,
                ornare condimentum mauris. Maecenas pellentesque, erat non pellentesque tincidunt,
                augue tortor sollicitudin libero, eu vestibulum est risus in elit. Pellentesque in bibendum nisi,
                quis ornare diam. Phasellus consectetur scelerisque libero, vel condimentum nulla consectetur sed.
                Proin vulputate nunc ut venenatis tempor. Duis pretium scelerisque eros vel euismod.
                Quisque iaculis cursus sapien, at rutrum dolor egestas tempus.
                Sed nec sapien id diam porttitor imperdiet et auctor lorem.
                Ut id posuere metus. Etiam molestie ultricies sem, sit amet fringilla arcu ornare at.
                Phasellus ac libero ornare, finibus diam et, mattis nunc.
                """
            )
        )

        if not self.user:
            return st.info("You don't have any active sessions.")

        st.success(f"Welcome {self.user.name}, you have an active session.")

        if st.button(label="Logout"):
            del st.session_state["token"]
            st.experimental_rerun()
