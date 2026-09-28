from typing import Literal
from pydantic import BaseModel, Field, field_validator
Goal = Literal["weight loss", "muscle gain", "general wellness", "flexibility"]
Intensity = Literal["low", "medium", "high"]
class UserInput(BaseModel):
    user_id: str = Field(min_length=2, max_length=64, pattern=r"^[A-Za-z0-9_-]+$")
    username: str = Field(min_length=2, max_length=120)
    age: int = Field(ge=13, le=120)
    weight: float = Field(gt=20, le=500)
    goal: Goal
    intensity: Intensity
    @field_validator("username")
    @classmethod
    def name(cls, value):
        value = value.strip()
        if not value: raise ValueError("Name cannot be blank")
        return value
class FeedbackRequest(BaseModel):
    user_id: str = Field(min_length=2, max_length=64)
    feedback: str = Field(min_length=3, max_length=1000)
    @field_validator("feedback")
    @classmethod
    def text(cls, value): return value.strip()
