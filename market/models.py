from enum import unique
from operator import length_hint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from .app import app, bcrypt, login_manager
from flask_login import UserMixin

db = SQLAlchemy(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), unique=True, nullable=False)
    email_address = db.Column(db.String(length=50),
                              unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def pw(self):
        return self.pw

    @pw.setter
    def pw(self, plain_text_pw):
        self.password = bcrypt.generate_password_hash(
            plain_text_pw).decode('utf-8')

    def check_password(self, password_entered):
        return bcrypt.check_password_hash(self.password, password_entered)

    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price

    @property
    def pretty_budget(self):
        if len(str(self.budget)) >= 4:
            return f"{str(self.budget)[:-3]},{str(self.budget)[-3:]}"
        else:
            return f"{self.budget}"


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(12), nullable=False, unique=True)
    description = db.Column(db.String(1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item {self.name}'

    def purchase_item(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()
