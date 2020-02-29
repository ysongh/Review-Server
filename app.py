from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "db.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    company = db.Column(db.String(100))
    tags = db.Column(db.String(200))
    description = db.Column(db.String(200))
    rating = db.Column(db.Integer)

    def __init__(self, name, company, tags, description, rating):
        self.name = name
        self.company = company
        self.tags = tags
        self.description = description
        self.rating = rating

# testing
@app.route("/", methods=["GET"])
def get():
    return jsonify({ "data": "Testing"})

if __name__ == "__main__":
    app.run(debug=True) 