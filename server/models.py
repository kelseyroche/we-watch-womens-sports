from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'  # For local development
db = SQLAlchemy(app)
CORS(app)  # Enable CORS for frontend/backend communication

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    bars = db.relationship('Bar', secondary='user_bars', backref='users')

# Bar Model
class Bar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    sports = db.relationship('Sport', secondary='bar_sports', backref='bars')
    streaming_services = db.relationship('StreamingService', secondary='bar_streaming', backref='bars')

# Sport Model
class Sport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

# StreamingService Model
class StreamingService(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

# Association table for many-to-many relationship between Bar and Sport
bar_sports = db.Table(
    'bar_sports',
    db.Column('bar_id', db.Integer, db.ForeignKey('bar.id'), primary_key=True),
    db.Column('sport_id', db.Integer, db.ForeignKey('sport.id'), primary_key=True)
)

# Association table for many-to-many relationship between Bar and StreamingService
bar_streaming = db.Table(
    'bar_streaming',
    db.Column('bar_id', db.Integer, db.ForeignKey('bar.id'), primary_key=True),
    db.Column('streaming_service_id', db.Integer, db.ForeignKey('streaming_service.id'), primary_key=True)
)

# Association table for many-to-many relationship between User and Bar (a user can follow many bars)
user_bars = db.Table(
    'user_bars',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('bar_id', db.Integer, db.ForeignKey('bar.id'), primary_key=True)
)

# Initialize the database (run this when you're first setting up your app)
def init_db():
    db.create_all()
    print("Database Initialized!")

if __name__ == "__main__":
    app.run(debug=True)