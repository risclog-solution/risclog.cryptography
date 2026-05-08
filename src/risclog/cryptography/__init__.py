from risclog.cryptography.fernet import (
    AirflowFernetCryptographyManager,
    CryptographyManager as FernetCryptographyManager,
)

# Fernet is the default
CryptographyManager = FernetCryptographyManager  # noqa

__all__ = [
    "AirflowFernetCryptographyManager",
    "CryptographyManager",
    "FernetCryptographyManager",
]
