import pytest
import enlil.server

@pytest.fixture
def config():
    return {}

@pytest.fixture
def app(config):
    app = enlil.server.create_app(config)
    return app
