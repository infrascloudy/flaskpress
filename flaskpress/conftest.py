import pytest
from flaskpress import create_app


@pytest.fixture
def app():
    app = create_app(config='flaskpress.test_settings',
                     DEBUG=False,
                     test=True,
                     mode='test')
    return app
