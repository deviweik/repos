# routes.py

from flask import Blueprint, jsonify, request
from app.models import db, User, Task
from werkzeug.security import generate_password_hash
from datetime import datetime

tasks_bp = Blueprint('tasks_bp', __name__, url_prefix='/tasks')
users_bp = Blueprint('users_bp', __name__, url_prefix='/users')

# Retrieve all tasks
@tasks_bp.route('/', methods=['GET'])
def get_all_tasks():
    tasks = Task.query.all()
    task_list = []
    for task in tasks:
        task_list.append({
            'id': task.id,
            'user_id': task.user_id,
            'title': task.title,
            'summary': task.summary,
            'created_date': task.created_date.strftime("%Y-%m-%d %H:%M:%S"),
            'due_date': task.due_date.strftime("%Y-%m-%d %H:%M:%S") if task.due_date else None,
            'priority': task.priority,
            'status': task.status,
            'category': task.category
        })
    return jsonify(task_list), 200

# Retrieve specific task details
@tasks_bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify({
        'id': task.id,
        'user_id': task.user_id,
        'title': task.title,
        'summary': task.summary,
        'created_date': task.created_date.strftime("%Y-%m-%d %H:%M:%S"),
        'due_date': task.due_date.strftime("%Y-%m-%d %H:%M:%S") if task.due_date else None,
        'priority': task.priority,
        'status': task.status,
        'category': task.category
    }), 200

# Create a new task
@tasks_bp.route('/', methods=['POST'])
def create_task():
    data = request.json
    try:
        created_date = datetime.strptime(data['created_date'], "%Y-%m-%d %H:%M:%S") if data['created_date'] else datetime.now()
        due_date = datetime.strptime(data['due_date'], "%Y-%m-%d %H:%M:%S") if data['due_date'] else None
    except ValueError:
        return jsonify({'message': 'Invalid date format. Please use YYYY-MM-DD HH:MM:SS format'}), 400

    new_task = Task(
        user_id=data['user_id'],
        title=data['title'],
        summary=data['summary'],
        created_date=created_date,
        due_date=due_date,
        priority=data['priority'],
        status=data['status'],
        category=data['category']
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({
        'message': 'Task created successfully',  
        'id': new_task.id,
        'user_id': new_task.user_id,
        'title': new_task.title
        }), 201

# Update an existing task
@tasks_bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.json
    task.user_id = data.get('user_id', task.user_id)
    task.title = data.get('title', task.title)
    task.summary = data.get('summary', task.summary)
    task.created_date = data.get('created_date', task.created_date)
    task.due_date = data.get('due_date', task.due_date)
    task.priority = data.get('priority', task.priority)
    task.status = data.get('status', task.status)
    task.category = data.get('category', task.category)
    db.session.commit()
    return jsonify({
        'message': 'Task updated successfully', 
        'id': task.id,
        'user_id': task.user_id,
        'title': task.title
        }), 200

# Delete a task
@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'}), 200

# Register a user
@users_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # reject blank fields
    if username == None or username == "":
        return jsonify({'message': 'Username is required'})
    if email == None or email == "":
        return jsonify({'message': 'Email is required'})
    if password == None or password == "":
        return jsonify({'message': 'Password is required'})

    # Check if username or email already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 400

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Create a new user
    new_user = User(
        username=username,
        email=email,
        password=hashed_password
    )

    # Add the user to the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'message': 'User registered successfully',  
        'id': new_user.id,
        'email': new_user.email,
        'username': new_user.username
        }), 201

# Retrieve all users
@users_bp.route('/', methods=['GET'])
def get_all_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_list.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'active_task_count': user.active_task_count,
            'on_hold_task_count': user.on_hold_task_count,
            'total_task_count': user.total_task_count,
            'role': user.role,
            'created_date': user.created_date
        })
    return jsonify(user_list), 200

# Retrieve a user's details
@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'active_task_count': user.active_task_count,
        'on_hold_task_count': user.on_hold_task_count,
        'total_task_count': user.total_task_count,
        'role': user.role,
        'created_date': user.created_date
    }), 200

# Update a user
@users_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json

    # only update non-null values
    if 'username' in data and data['username'] is not None:
        new_username = data['username']
        if new_username != user.username and User.query.filter_by(username=new_username).first():
            return jsonify({'message': 'Username already exists'}), 400
        user.username = new_username

    if 'email' in data and data['email'] is not None:
        new_email = data['email']
        if new_email != user.email and User.query.filter_by(email=new_email).first():
            return jsonify({'message': 'Email already exists'}), 400
        user.email = new_email

    if 'password' in data and data['password'] is not None:
        hashed_password = generate_password_hash(data['password'])
        user.password = hashed_password
    
    if 'first_name' in data and data['first_name'] is not None:
        user.first_name = data.get('first_name', user.first_name)

    if 'last_name' in data and data['last_name'] is not None:
        user.last_name = data.get('last_name', user.last_name)

    if 'active_task_count' in data and data['active_task_count'] is not None:
        user.active_task_count = data.get('active_task_count', user.active_task_count)

    if 'on_hold_task_count' in data and data['on_hold_task_count'] is not None:
        user.on_hold_task_count = data.get('on_hold_task_count', user.on_hold_task_count)

    if 'total_task_count' in data and data['total_task_count'] is not None:
        user.total_task_count = data.get('total_task_count', user.total_task_count)
    
    if 'role' in data and data['role'] is not None:
        user.role = data.get('role', user.role)

    if 'created_date' in data and data['created_date'] is not None:
        user.created_date = data.get('created_date', user.created_date)

    db.session.commit()

    return jsonify({
        'message': 'User updated successfully',  
        'id': user.id,
        'email': user.email,
        'username': user.username
        }), 200

# Delete a user
@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200
