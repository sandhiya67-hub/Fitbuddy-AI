from .gemini_client import workout
from .schemas import UserInput
def update_workout_plan(original_plan: str, feedback: str, user: UserInput) -> str:
    fallback=lambda:"LOCAL DEVELOPMENT UPDATED PLAN (Gemini key not configured)\nFeedback received: "+feedback+"\nApply the requested adjustment gradually, preserve rest days, and stop if activity causes pain.\n\n"+original_plan
    prompt=f"Revise this complete 7-day plan for {user.username}, goal {user.goal}, intensity {user.intensity}. Feedback: {feedback}\n\nOriginal plan:\n{original_plan}\n\nReturn a safe complete revised 7-day plan with warm-ups, cooldowns, and recovery; no medical advice."
    return workout(prompt,fallback)
