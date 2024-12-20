import pytest

from decouple import Config, RepositoryEnv


@pytest.fixture
def api_key():
    config = Config(RepositoryEnv(".env"))
    api_key = config("OPENAI_API_KEY")
    return api_key
