from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "db.sqlite")
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://xlpzivwlnakcfv:66446c4d45073cf9382db02161ae90e77767634367e0565f934b21da624bec53@ec2-35-168-54-239.compute-1.amazonaws.com:5432/dacg48onjdl0a2"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    company = db.Column(db.String(100))
    image = db.Column(db.String(100))
    tags = db.Column(db.String(200))
    description = db.Column(db.String(200))
    rating = db.Column(db.Float)

    def __init__(self, name, company, image, tags, description, rating):
        self.name = name
        self.company = company
        self.image = image
        self.tags = tags
        self.description = description
        self.rating = rating

class PersonSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "company", "image", "tags", "description", "rating")

person_schema = PersonSchema()
persons_schema = PersonSchema(many = True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    person_id = db.Column(db.Integer)
    author = db.Column(db.String(100))
    comment = db.Column(db.String(200))
    tags = db.Column(db.String(200))
    rating = db.Column(db.Float)

    def __init__(self, person_id, author, comment, tags, rating):
        self.person_id = person_id
        self.author = author
        self.comment = comment
        self.tags = tags
        self.rating = rating

class ReviewSchema(ma.Schema):
    class Meta:
        fields = ("id", "person_id", "author", "comment", "tags", "rating")

reviews_schema = ReviewSchema(many = True)

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
    image = request.json["image"]
    tags = request.json["tags"]
    description = request.json["description"]
    rating = request.json["rating"]

    new_person = Person(name, company, image, tags, description, rating)

    db.session.add(new_person)
    db.session.commit()

    return person_schema.jsonify(new_person)

# find person by Id
@app.route("/person/<id>", methods=["GET"])
def get_person(id):
    person = Person.query.get(id)
    return person_schema.jsonify(person)

if __name__ == "__main__":
    app.run(debug=True)