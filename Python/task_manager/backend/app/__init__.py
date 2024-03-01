# __init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task_manager.db'
db = SQLAlchemy(app)
# migrate = Migrate(app, db)

from .routes import tasks_bp, users_bp  # Import Blueprints after app is created to avoid circular imports

# Register Blueprints
app.register_blueprint(tasks_bp)
app.register_blueprint(users_bp)
