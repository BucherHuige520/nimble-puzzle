from flask import Flask

app = Flask("Nimble Puzzle")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///nimble.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
