from nimble.app import app
from nimble.db import db


def main():
    from nimble import apis
    with app.app_context():
        db.create_all()
    apis.init()
    app.run()


if __name__ == "__main__":
    main()
