import json, os

def _fallback(goal, level, days):
    return {'workout_plan': f'Goal: {goal}\nLevel: {level}\n{days}-day schedule\nDay 1: Full-body strength (squat, push-up, row) - 3x10\nDay 2: Cardio and mobility - 25 minutes\nDay 3: Full-body strength and core - 3x10', 'nutrition_tips': 'Prioritize protein with every meal, eat colorful vegetables, hydrate regularly, and match portions to your goal.'}

def generate_plan(goal, level='beginner', days=3):
    key=os.getenv('GEMINI_API_KEY')
    if not key: return _fallback(goal, level, days)
    try:
        from google import genai
        client=genai.Client(api_key=key)
        prompt=f'Return JSON with workout_plan and nutrition_tips for a safe fitness plan. Goal={goal}, level={level}, days={days}.'
        response=client.models.generate_content(model=os.getenv('GEMINI_MODEL','gemini-2.0-flash'), contents=prompt)
        text=response.text.strip().replace('```json','').replace('```','')
        return json.loads(text)
    except Exception:
        return _fallback(goal, level, days)

def update_plan(plan, feedback):
    plan.workout_plan += f'\n\nUpdate based on feedback: {feedback}'
    plan.feedback = feedback
    return plan
