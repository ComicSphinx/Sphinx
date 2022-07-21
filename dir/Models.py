# @Author: Daniil Maslov (ComicSphinx)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from matplotlib.style import use

app = Flask(__name__)
db = SQLAlchemy(app)

class BudgetFields(db.Model):
    __tablename__   = "budgetFields"
    id              = db.Column(db.Integer, primary_key=True)
    userId          = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.String, nullable = False)
    active          = db.Column(db.Boolean, nullable = False)

    def __init__(self, id, userId, name, active):
        self.id = id
        self.userId = userId
        self.name = name
        self.active = active

    def serialize(self):
        return {
            'id': self.id,
            'userId': self.userId,
            'name': self.name,
            'active': self.active
        }

class Budget(db.model):
    __tablename__   = "budget"
    id              = db.Column(db.Integer, primary_key=True)
    userId          = db.Column(db.Integer, primary_key=True)
    budgetFieldId   = db.Column(db.Integer, primary_key=True)
    value           = db.Column(db.String, nullable = False)
    active          = db.Column(db.Boolean, nullable = False)

    def __init__(self, id, userId, budgetFieldId, value, active):
        self.id = id
        self.userId = userId
        self.budgetFieldId = budgetFieldId
        self.value = value
        self.active = active

    def serialize(self):
        return {
            'id': self.id,
            'userId': self.userId,
            'budgetFieldId': self.budgetFieldId,
            'value': self.value,
            'active': self.active
        }