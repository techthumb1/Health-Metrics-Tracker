# app/models.py
from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Metrics(db.Model):
    id = Column(Integer, primary_key=True)
    date_logged = Column(DateTime, default=datetime.utcnow)
    heart_rate = Column(Float)
    blood_pressure = Column(String)  # e.g., "120/80"
    weight = Column(Float)
    sleep_quality = Column(Integer)  # Scale: 1-10
    hydration = Column(Float)  # Liters
    activity_level = Column(Float)  # Steps or minutes of exercise
    blood_glucose = Column(Float)  # mg/dL
    oxygen_saturation = Column(Float)  # Percentage
    cholesterol = Column(Float)  # mg/dL
    
