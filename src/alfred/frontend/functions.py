from typing import Dict, Optional

import streamlit as st

from alfred.models.user import User


def get_session_payload(token: str, disable_expiration: bool = False) -> Dict:
    from alfred.utils.json_web_token import JsonWebToken

    jwt = JsonWebToken.auto_configure(verify_exp=not disable_expiration)
    return jwt.decode(token)


def get_user(
        disable_token_expiration: bool = False,
) -> Optional[User]:
    token = st.session_state.get("token")
    if not token:
        return
    payload = get_session_payload(
        token=token,
        disable_expiration=disable_token_expiration
    )
    return User.get(email=payload["user"])


def get_user_with_warning(
        disable_token_expiration: bool = False,
        disable_message: bool = False,
        message: Optional[str] = None,
) -> Optional[User]:
    user = get_user(disable_token_expiration=disable_token_expiration)
    if not user:
        if not disable_message:
            st.error(
                message or (
                    "You must have an active session to visualize this content."
                )
            )
        return
    return user
