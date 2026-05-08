import asyncio
import base64
import os
from typing import Any, Coroutine, Optional, Union, cast

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class CryptographyManager:
    def __init__(
        self,
        password: Union[str, bytes],
        salt: Optional[Union[str, bytes]] = None,
        iterations: int = 400000,
    ):
        """
        Initialize the CryptographyManager with the given parameters.

        :param password: The password used for key derivation.
        :param salt: The salt to use for PBKDF2. If None, a new salt is generated.
        :param iterations: The number of iterations for PBKDF2.
        """
        self.password = (
            password if isinstance(password, bytes) else str.encode(password)
        )
        if salt:
            self.salt: bytes = (
                salt
                if isinstance(salt, bytes)
                else str.encode(salt).decode("unicode_escape").encode()
            )
        else:
            self.salt = os.urandom(16)

        self.iterations = iterations
        self.key_length = 32  # Length of the derived key in bytes (for Fernet)

        # Create PBKDF2HMAC instance
        self.kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=self.key_length,
            salt=self.salt,
            iterations=self.iterations,
            backend=default_backend(),
        )

        # Derive a key from the password
        self.key = self.kdf.derive(self.password)

        # Encode the key in Base64 for Fernet
        self.encoded_key = base64.urlsafe_b64encode(self.key)

        # Create Fernet instance with the derived key
        self.fernet = Fernet(self.encoded_key)

    async def __aencrypt(self, message: Union[str, bytes]) -> bytes:
        """
        Encrypt the given message using Fernet asynchronously.

        :param message: The message to encrypt.
        :return: The encrypted message.
        """
        message = message if isinstance(message, bytes) else str.encode(message)
        return cast(bytes, await asyncio.to_thread(self.fernet.encrypt, message))

    async def __adecrypt(self, token: bytes) -> str:
        """
        Decrypt the given token using Fernet asynchronously.

        :param token: The encrypted message to decrypt.
        :return: The decrypted message.
        """
        message = cast(bytes, await asyncio.to_thread(self.fernet.decrypt, token))
        return message.decode()

    def encrypt(
        self, message: Union[str, bytes]
    ) -> Union[bytes, Coroutine[Any, Any, bytes]]:
        """
        Encrypt the given message using Fernet.

        When called from within a running event loop, returns a coroutine that must be awaited.
        When called outside an event loop, returns the encrypted bytes directly.

        :param message: The message to encrypt.
        :return: Encrypted bytes, or a coroutine yielding encrypted bytes if called from a running loop.
        """
        try:
            loop: Optional[asyncio.AbstractEventLoop] = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            return self.__aencrypt(message=message)
        else:
            return asyncio.run(self.__aencrypt(message=message))

    def decrypt(self, token: bytes) -> Union[str, Coroutine[Any, Any, str]]:
        """
        Decrypt the given token using Fernet.

        When called from within a running event loop, returns a coroutine that must be awaited.
        When called outside an event loop, returns the decrypted string directly.

        :param token: The encrypted message to decrypt.
        :return: Decrypted string, or a coroutine yielding decrypted string if called from a running loop.
        """
        try:
            loop: Optional[asyncio.AbstractEventLoop] = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            return self.__adecrypt(token=token)
        else:
            return asyncio.run(self.__adecrypt(token=token))


class AirflowFernetCryptographyManager:
    """Native Airflow-Fernet compatible encryption.

    Airflow stores Fernet keys as 32-byte url-safe base64 strings in
    ``AIRFLOW__CORE__FERNET_KEY``. This manager uses that key directly and
    intentionally does not derive a new key from password/salt.
    """

    def __init__(self, key: Union[str, bytes]):
        self.key = key if isinstance(key, bytes) else str.encode(key)
        self.fernet = Fernet(self.key)

    @staticmethod
    def generate_key() -> bytes:
        """Generate a native Airflow-compatible Fernet key."""
        return cast(bytes, Fernet.generate_key())

    @classmethod
    def from_env(
        cls, env_name: str = "AIRFLOW__CORE__FERNET_KEY"
    ) -> "AirflowFernetCryptographyManager":
        """Create a manager from an environment variable."""
        key = os.getenv(env_name)
        if not key:
            raise RuntimeError(f"Missing Fernet key environment variable: {env_name}")
        return cls(key)

    def encrypt(self, message: Union[str, bytes]) -> bytes:
        """Encrypt *message* and return a native ``gAAAA...`` Fernet token."""
        value = message if isinstance(message, bytes) else str.encode(message)
        return cast(bytes, self.fernet.encrypt(value))

    def decrypt(self, token: Union[str, bytes]) -> str:
        """Decrypt a native Airflow-Fernet token."""
        value = token if isinstance(token, bytes) else str.encode(token)
        return cast(str, self.fernet.decrypt(value).decode())
