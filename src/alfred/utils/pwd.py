import posixpath
import hashlib
import secrets
import string
from typing import Tuple

from alfred.settings import (
    ALFRED_DEFAULT_SALT_LENGTH,
    ALFRED_SECRET,
)


def get_salt(length: int = ALFRED_DEFAULT_SALT_LENGTH) -> str:
    options = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return "".join(secrets.choice(options) for _ in range(length))


def password_hash(pwd: str, salt: str) -> str:
    raw = posixpath.join(ALFRED_SECRET, salt, pwd).encode(encoding="utf-8")
    return hashlib.sha256(raw).hexdigest()


def password_cooking(pwd: str, salt_length: int = ALFRED_DEFAULT_SALT_LENGTH) -> Tuple[str, str]:
    # How do you cook a password? You add some salt and hash it.
    salt = get_salt(length=salt_length)
    return password_hash(pwd=pwd, salt=salt), salt
