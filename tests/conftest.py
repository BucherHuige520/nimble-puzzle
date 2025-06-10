import pytest
from nimble import apis
from nimble.app import app as nimble_app
from nimble.db import db, Task


@pytest.fixture()
def app():
    nimble_app.testing = True
    nimble_app.config.update({
        "SQLALCHEMY_DATABASE_URI": "sqlite:///nimble-test.sqlite"
    })
    apis.init()

    with nimble_app.app_context():
        db.create_all()
        Task.query.delete()
        db.session.commit()
    yield nimble_app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
