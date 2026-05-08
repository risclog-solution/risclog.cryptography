import os

import pytest
from cryptography.fernet import InvalidToken
from risclog.cryptography import (
    AirflowFernetCryptographyManager,
    CryptographyManager,
)


@pytest.mark.asyncio
async def test_async_cryptography_manager():
    password = b"fSaCbrwrNZt0TYumhzbAOCQl2Trp2siFqXa-rowb4l8="
    message = b"Secret message!"
    salt = os.urandom(16)

    crypto_manager = CryptographyManager(password=password, salt=salt)

    token = await crypto_manager.encrypt(message)
    assert token is not None

    decrypted_message = await crypto_manager.decrypt(token)
    assert decrypted_message == message.decode()


@pytest.mark.asyncio
async def test_async_cryptography_manager_invalid_token():
    salt = os.urandom(16)
    password = b"fSaCbrwrNZt0TYumhzbAOCQl2Trp2siFqXa-rowb4l8="
    invalid_token = b"InvalidToken"
    crypto_manager = CryptographyManager(password=password, salt=salt)

    with pytest.raises(InvalidToken):
        await crypto_manager.decrypt(invalid_token)


@pytest.mark.asyncio
async def test_async_cryptography_manager_with_salt_not_set():
    password = b"fSaCbrwrNZt0TYumhzbAOCQl2Trp2siFqXa-rowb4l8="
    message = b"Secret message!"

    crypto_manager = CryptographyManager(password=password)

    token = await crypto_manager.encrypt(message)
    assert token is not None

    decrypted_message = await crypto_manager.decrypt(token)
    assert decrypted_message == message.decode()


@pytest.mark.asyncio
async def test_async_cryptography_manager_with_salt_not_set_and_second_cryptography_manager_instance():
    password = b"fSaCbrwrNZt0TYumhzbAOCQl2Trp2siFqXa-rowb4l8="
    message = b"Secret message!"

    crypto_manager = CryptographyManager(password=password)
    token = await crypto_manager.encrypt(message)
    assert token is not None

    crypto_manager = CryptographyManager(password=password)
    with pytest.raises(InvalidToken):
        await crypto_manager.decrypt(token)


def test_cryptography_manager():
    password = b"fSaCbrwrNZt0TYumhzbAOCQl2Trp2siFqXa-rowb4l8="
    message = b"Secret message!"
    salt = os.urandom(16)

    crypto_manager = CryptographyManager(password=password, salt=salt)

    token = crypto_manager.encrypt(message)
    assert token is not None

    decrypted_message = crypto_manager.decrypt(token)
    assert decrypted_message == message.decode()


def test_cryptography_manager_invalid_token():
    salt = os.urandom(16)
    password = b"fSaCbrwrNZt0TYumhzbAOCQl2Trp2siFqXa-rowb4l8="
    invalid_token = b"InvalidToken"
    crypto_manager = CryptographyManager(password=password, salt=salt)

    with pytest.raises(InvalidToken):
        crypto_manager.decrypt(invalid_token)


def test_airflow_fernet_cryptography_manager_roundtrip():
    key = AirflowFernetCryptographyManager.generate_key()
    crypto_manager = AirflowFernetCryptographyManager(key)

    token = crypto_manager.encrypt("Secret message!")

    assert token.startswith(b"gAAAA")
    assert crypto_manager.decrypt(token) == "Secret message!"
    assert crypto_manager.decrypt(token.decode()) == "Secret message!"


def test_airflow_fernet_cryptography_manager_from_env(monkeypatch):
    key = AirflowFernetCryptographyManager.generate_key().decode()
    monkeypatch.setenv("AIRFLOW__CORE__FERNET_KEY", key)

    crypto_manager = AirflowFernetCryptographyManager.from_env()
    token = crypto_manager.encrypt(b"Secret message!")

    assert crypto_manager.decrypt(token) == "Secret message!"


def test_airflow_fernet_cryptography_manager_from_env_missing(monkeypatch):
    monkeypatch.delenv("AIRFLOW__CORE__FERNET_KEY", raising=False)

    with pytest.raises(RuntimeError, match="AIRFLOW__CORE__FERNET_KEY"):
        AirflowFernetCryptographyManager.from_env()


def test_airflow_fernet_cryptography_manager_invalid_token():
    crypto_manager = AirflowFernetCryptographyManager(
        AirflowFernetCryptographyManager.generate_key()
    )

    with pytest.raises(InvalidToken):
        crypto_manager.decrypt("InvalidToken")
