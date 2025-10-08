from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db, bcrypt
from models import User, Book
from utils import admin_required
from models import Book, Author
from datetime import datetime
from app import photos, db
from werkzeug.utils import secure_filename
import os


auth_bp = Blueprint('auth', __name__)
books_bp = Blueprint('books', __name__)

# --- Authentication Routes ---
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully!"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token)
    return jsonify({"message": "Invalid username or password"}), 401

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if user:
        return jsonify({
            "username": user.username,
            "email": user.email,
            "is_admin": user.is_admin,
            "avatar_url": user.avatar_url
        })
    return jsonify({"message": "User not found"}), 404

# --- Book Management Routes (for Admin) ---
@books_bp.route('/', methods=['POST'])
@jwt_required()
@admin_required() # Add this decorator
def add_book():
    data = request.get_json()
    try:
        new_book = Book(
            title=data['title'],
            published_date=datetime.strptime(data['published_date'], '%Y-%m-%d').date(),
            isbn=data['isbn'],
            author_id=data['author_id']
        )
        db.session.add(new_book)
        db.session.commit()
        return jsonify({"message": "Book added successfully!", "book_id": new_book.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@books_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_books():
    books = Book.query.all()
    books_list = [{
        "id": book.id,
        "title": book.title,
        "author": book.author.name,
        "published_date": book.published_date.strftime('%Y-%m-%d'),
        "isbn": book.isbn,
        "is_available": book.is_available
    } for book in books]
    return jsonify(books_list)

@books_bp.route('/<int:book_id>', methods=['DELETE'])
@jwt_required()
@admin_required()
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully"}), 200

# --- Profile Routes ---
@auth_bp.route('/update-profile', methods=['PUT'])
@jwt_required()
def update_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.form
    if 'username' in data:
        user.username = data['username']

    if 'email' in data:
        user.email = data['email']

    # Handle avatar upload
    if 'avatar' in request.files:
        filename = photos.save(request.files['avatar'])
        user.avatar_url = os.path.join('/static/avatars', filename)

    db.session.commit()
    return jsonify({
        "message": "Profile updated successfully",
        "username": user.username,
        "email": user.email,
        "avatar_url": user.avatar_url
    })
