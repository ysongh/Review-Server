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

class PersonSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "company", "tags", "description", "rating")

person_schema = PersonSchema()
persons_schema = PersonSchema(many = True)

# testing
@app.route("/", methods=["GET"])
def get():
    return jsonify({ "data": "Testing"})

# get all person
@app.route("/person", methods=["GET"])
def get_persons():
    all_persons = Person.query.all()
    result = persons_schema.dump(all_persons)

    return jsonify(result)

# add a person
@app.route("/person", methods=["POST"])
def add_person():
    name = request.json["name"]
    company = request.json["company"]
    tags = request.json["tags"]
    description = request.json["description"]
    rating = request.json["rating"]

    new_person = Person(name, company, tags, description, rating)

    db.session.add(new_person)
    db.session.commit()

    return person_schema.jsonify(new_person)

if __name__ == "__main__":
    app.run(debug=True)