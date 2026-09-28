from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__='users'
    id=Column(Integer, primary_key=True)
    name=Column(String(120), nullable=False)
    email=Column(String(255), unique=True, nullable=False)
    created_at=Column(DateTime, default=datetime.utcnow)
    plans=relationship('FitnessPlan', back_populates='user', cascade='all, delete-orphan')

class FitnessPlan(Base):
    __tablename__='fitness_plans'
    id=Column(Integer, primary_key=True)
    user_id=Column(Integer, ForeignKey('users.id'), nullable=False)
    goal=Column(String(120), nullable=False)
    level=Column(String(50), default='beginner')
    days_per_week=Column(Integer, default=3)
    workout_plan=Column(Text, nullable=False)
    nutrition_tips=Column(Text, nullable=False)
    feedback=Column(Text)
    created_at=Column(DateTime, default=datetime.utcnow)
    user=relationship('User', back_populates='plans')
