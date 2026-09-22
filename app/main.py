import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
MOCK_AI = os.getenv("MOCK_AI", "true").lower() == "true"


def generate_workout(
    username: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str
):
    """
    Generate a personalized 7-day workout plan.
    """

    # Demo mode
    if MOCK_AI or not GEMINI_API_KEY:
        return generate_demo_workout(
            username,
            age,
            weight,
            goal,
            intensity
        )

    prompt = f"""
You are FitBuddy, an AI fitness planning assistant.

Create a personalized 7-day fitness plan for the following user.

User name: {username}
Age: {age}
Weight: {weight} kg
Fitness goal: {goal}
Workout intensity: {intensity}

Requirements:

1. Create exactly 7 days.
2. Include warm-up.
3. Include the main workout.
4. Include sets, repetitions, or duration.
5. Include rest periods.
6. Include cool-down/recovery.
7. Include at least one rest or recovery day.
8. Adapt the plan to the user's fitness goal.
9. Adapt the difficulty to the selected intensity.
10. Keep the plan practical for a normal beginner/intermediate user.
11. Do not diagnose medical conditions.
12. Add basic safety advice.

Use this format:

DAY 1
Warm-up:
Workout:
Sets/Reps:
Rest:
Cool-down:

DAY 2
...

Continue until DAY 7.

At the end provide:

NUTRITION TIPS
- tip 1
- tip 2
- tip 3

RECOVERY TIPS
- tip 1
- tip 2
- tip 3
"""

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        return response.text

    except Exception as error:
        return f"""
AI generation failed.

Error:
{error}

Please check your Gemini API key and internet connection.
"""


def generate_demo_workout(
    username: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str
):
    """
    Demo workout used when MOCK_AI=true.
    """

    return f"""
# FitBuddy 7-Day Fitness Plan

**User:** {username}

**Age:** {age}

**Weight:** {weight} kg

**Goal:** {goal}

**Intensity:** {intensity}

---

## DAY 1 - Full Body Strength

**Warm-up**
- 5 minutes walking
- Arm circles
- Bodyweight squats

**Workout**
- Squats: 3 × 12
- Push-ups: 3 × 8
- Lunges: 3 × 10 each leg
- Plank: 3 × 30 seconds

**Rest:** 60 seconds between sets.

**Cool-down**
- 5 minutes of stretching.

---

## DAY 2 - Cardio

**Warm-up**
- 5 minutes light walking.

**Workout**
- Brisk walking: 20 minutes
- Jumping jacks: 3 × 20
- High knees: 3 × 20 seconds

**Rest:** 45-60 seconds.

**Cool-down**
- Walking and stretching.

---

## DAY 3 - Upper Body

**Warm-up**
- Arm rotations
- Shoulder mobility

**Workout**
- Push-ups: 3 × 10
- Chair dips: 3 × 10
- Shoulder taps: 3 × 12
- Plank: 3 × 30 seconds

**Cool-down**
- Shoulder and arm stretches.

---

## DAY 4 - Recovery Day

Take a recovery day.

Recommended:
- 20-30 minute easy walk
- Light stretching
- Good hydration
- Adequate sleep

---

## DAY 5 - Lower Body

**Warm-up**
- 5 minutes walking
- Dynamic leg stretches

**Workout**
- Squats: 3 × 15
- Lunges: 3 × 10 each leg
- Glute bridges: 3 × 15
- Calf raises: 3 × 15

**Cool-down**
- Lower-body stretching.

---

## DAY 6 - Full Body Circuit

Complete 3 rounds:

- 15 squats
- 10 push-ups
- 10 lunges each leg
- 20 jumping jacks
- 30-second plank

Rest 1-2 minutes between rounds.

---

## DAY 7 - Active Recovery

- 20 minutes walking
- Full-body stretching
- Breathing exercises
- Hydration
- Rest

---

# NUTRITION TIPS

- Eat enough protein from foods such as eggs, milk, beans, lentils, fish or lean meat.
- Include vegetables and fruits in your daily meals.
- Drink enough water.
- Prefer balanced meals over highly processed foods.
- Adjust portion sizes according to your personal needs and activity level.

# RECOVERY TIPS

- Aim for consistent sleep.
- Drink water throughout the day.
- Take rest when you feel unusually fatigued.
- Stretch gently after workouts.
- Increase exercise difficulty gradually.
"""


def update_workout(
    username: str,
    goal: str,
    intensity: str,
    old_plan: str,
    feedback: str
):
    """
    Update an existing workout plan based on user feedback.
    """

    if MOCK_AI or not GEMINI_API_KEY:
        return generate_updated_demo(
            username,
            goal,
            intensity,
            feedback
        )

    prompt = f"""
You are FitBuddy AI.

The user already has a 7-day workout plan.

User:
Name: {username}
Goal: {goal}
Intensity: {intensity}

CURRENT PLAN:
{old_plan}

USER FEEDBACK:
{feedback}

Create a revised 7-day workout plan.

Use the feedback to modify the plan.

Requirements:
- Keep exactly 7 days.
- Keep the user's fitness goal.
- Adjust exercises according to feedback.
- Adjust intensity where necessary.
- Include warm-up.
- Include workout.
- Include sets/reps/duration.
- Include rest.
- Include cool-down.
- Include recovery.
- Include at least one recovery/rest day.
- Do not provide medical diagnosis.

Clearly provide the updated plan.
"""

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        return response.text

    except Exception as error:
        return f"Unable to update the plan: {error}"


def generate_updated_demo(
    username: str,
    goal: str,
    intensity: str,
    feedback: str
):
    return f"""
# Updated FitBuddy Plan

**User:** {username}

**Goal:** {goal}

**Intensity:** {intensity}

### Changes based on your feedback

> {feedback}

---

## DAY 1
Full-body workout with a 5-minute warm-up.

- Squats: 3 × 10
- Push-ups: 3 × 8
- Lunges: 3 × 8 each leg
- Plank: 3 × 20 seconds

## DAY 2
Light cardio.

- 20-minute walking
- Light stretching

## DAY 3
Upper-body workout.

- Push-ups: 3 × 8
- Shoulder taps: 3 × 10
- Chair dips: 3 × 8

## DAY 4
REST AND RECOVERY

- Easy walking
- Stretching
- Hydration

## DAY 5
Lower-body workout.

- Squats: 3 × 12
- Glute bridges: 3 × 12
- Calf raises: 3 × 15

## DAY 6
Light full-body circuit.

Complete 2-3 rounds:

- Squats
- Push-ups
- Lunges
- Plank

## DAY 7
Active recovery.

- Walking
- Stretching
- Breathing exercises

---

## Recovery

Get adequate sleep, drink water, and increase exercise intensity gradually.
"""