import pytest
import os
from ya_disk import YaUploader:
from dogs import Dogs


@pytest.fixture()
def yandex_client():
	return YaUploader(os.getenv("TOKEN"))


@pytest.fixture()
def dogs(yandex_client):
	return Dogs(yandex_client)
