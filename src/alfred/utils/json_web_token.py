from typing import Any, Dict, Optional

from alfred.settings import (
    ALFRED_JWT_ENCRYPTION_ALGO,
    get_jwt_secret_key
)


class JsonWebToken:

    def __init__(
            self,
            secret_key: str,
            algorithm: Optional[str] = None,
            verify_exp: bool = False,
    ):
        self._secret_key = secret_key
        self.verify_exp = verify_exp
        self.algorithm: str = algorithm or ALFRED_JWT_ENCRYPTION_ALGO

    @classmethod
    def auto_configure(cls, verify_exp: bool = False) -> 'JsonWebToken':
        return cls(
            secret_key=get_jwt_secret_key(),
            algorithm=ALFRED_JWT_ENCRYPTION_ALGO,
            verify_exp=verify_exp
        )

    def encode(self, payload: Dict) -> str:
        import jwt  # type: ignore  # Lazy import
        return jwt.encode(
            payload,
            key=self._secret_key,
            algorithm=self.algorithm
        )

    def decode(self, string: str) -> Dict[str, Any]:
        import jwt  # type: ignore  # Lazy import
        return jwt.decode(
            jwt=string,
            key=self._secret_key,
            algorithms=[self.algorithm],
            options={
                "verify_exp": self.verify_exp
            }
        )
