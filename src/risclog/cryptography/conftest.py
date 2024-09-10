import mock
import pytest


class TestSettings:
    package_name: str = "risclog.cryptography"
    debug: bool = True


@pytest.fixture(autouse=True)
def settings():
    with mock.patch(
        "risclog.fastapi.config.MetadataSettings", side_effect=TestSettings
    ):
        with mock.patch(
            "risclog.cryptography.config.Settings", side_effect=TestSettings
        ):
            yield
