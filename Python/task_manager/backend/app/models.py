# models.py

from flask_sqlalchemy import SQLAlchemy
from app import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    active_task_count = db.Column(db.Integer)
    on_hold_task_count = db.Column(db.Integer)
    total_task_count = db.Column(db.Integer)
    role = db.Column(db.String(30))
    created_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    summary = db.Column(db.Text)
    created_date = db.Column(db.DateTime, nullable=False)
    due_date = db.Column(db.DateTime)
    priority = db.Column(db.String(100))
    status = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)

    user = db.relationship('User', backref=db.backref('tasks', lazy=True))

    def __repr__(self):
        return f"Task(id={self.id}, title={self.title}, user_id={self.user_id})"
