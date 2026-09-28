from .gemini_client import workout
from .schemas import UserInput
def generate_workout_gemini(data: UserInput) -> str:
    def fallback():
        days = [("Full-body foundation", "Squats, incline push-ups, rows, brisk walk"),("Cardio and mobility", "Easy cardio plus hip and shoulder mobility"),("Strength focus", "Split squats, presses, hinges, plank"),("Active recovery", "Gentle walk, yoga, or light stretching"),("Full-body circuit", "Squat, push, pull, hinge, and carry"),("Goal-focused conditioning", "Comfortable intervals or low-impact session"),("Rest and reset", "Rest with optional gentle mobility")]
        lines=["LOCAL DEVELOPMENT PLAN (Gemini key not configured)",f"Goal: {data.goal.title()} | Intensity: {data.intensity.title()}","Use comfortable effort and stop if you feel pain.",""]
        for i,(focus,work) in enumerate(days,1): lines += [f"Day {i} - {focus}","Warm-up: 5-10 minutes of easy movement.",f"Main workout: {work}.","Cooldown: 5 minutes of gentle stretching.",""]
        return "\n".join(lines)
    prompt=f"Create a safe structured 7-day workout plan for a {data.age}-year-old, {data.weight} kg person. Goal: {data.goal}; intensity: {data.intensity}. Each day needs a focus, 5-10 minute warm-up, exercises with sets/reps or duration, and cooldown. Include recovery and avoid medical advice."
    return workout(prompt, fallback)
