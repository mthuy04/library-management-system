from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    avatar_url = db.Column(db.String(255), default='default-avatar.png')

class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # Relationship
    books = db.relationship('Book', backref='author', lazy=True)

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    published_date = db.Column(db.Date, nullable=False)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    # Foreign Key
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
