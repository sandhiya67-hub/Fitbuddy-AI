from html import escape
from pathlib import Path

from fastapi import APIRouter, FastAPI, Form, Request
from fastapi.responses import HTMLResponse

try:
    from .main import generate_workout, update_workout
except ImportError:
    from main import generate_workout, update_workout


router = APIRouter()
users = {}
TEMPLATE_PATH = Path(__file__).resolve().parent.parent / "templates" / "index.html"


def render_page(title: str, content: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape(title)}</title>
    <style>
        body {{ margin: 0; font-family: Arial, sans-serif; background: #f1f8f4; color: #18352a; }}
        .container {{ max-width: 700px; margin: 50px auto; padding: 30px; background: white; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.1); }}
        h1 {{ text-align: center; color: #0d5c3b; }}
        pre {{ white-space: pre-wrap; line-height: 1.5; }}
        textarea {{ width: 100%; box-sizing: border-box; padding: 12px; }}
        button {{ width: 100%; padding: 14px; margin-top: 25px; border: none; border-radius: 7px; background: #0d5c3b; color: white; font-size: 16px; cursor: pointer; }}
        a {{ color: #0d5c3b; }}
    </style>
</head>
<body><div class="container">{content}</div></body>
</html>"""


@router.get("/", response_class=HTMLResponse)
async def home() -> HTMLResponse:
    return HTMLResponse(content=TEMPLATE_PATH.read_text(encoding="utf-8"))


@router.post("/generate-workout", response_class=HTMLResponse)
async def generate_workout_plan(
    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
) -> HTMLResponse:
    plan = generate_workout(username, age, weight, goal, intensity)
    users[user_id] = {
        "username": username,
        "user_id": user_id,
        "age": age,
        "weight": weight,
        "goal": goal,
        "intensity": intensity,
        "plan": plan,
        "original_plan": plan,
        "feedback": "",
    }
    return HTMLResponse(content=render_page("Your Fitness Plan", result_page(users[user_id])))


@router.post("/submit-feedback", response_class=HTMLResponse)
async def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    username: str = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    old_plan: str = Form(...),
    feedback: str = Form(...),
) -> HTMLResponse:
    updated_plan = update_workout(
        username=username,
        goal=goal,
        intensity=intensity,
        old_plan=old_plan,
        feedback=feedback,
    )

    users[user_id] = {
        "username": username,
        "user_id": user_id,
        "age": "",
        "weight": "",
        "goal": goal,
        "intensity": intensity,
        "plan": updated_plan,
        "original_plan": old_plan,
        "feedback": feedback,
    }

    return HTMLResponse(
        content=render_page("Updated Fitness Plan", result_page(users[user_id]))
    )


def result_page(user: dict) -> str:
    username = escape(str(user["username"]))
    user_id = escape(str(user["user_id"]))
    goal = escape(str(user["goal"]))
    intensity = escape(str(user["intensity"]))
    plan = escape(str(user["plan"]))

    return f"""
        <h1>Updated Fitness Plan</h1>
        <h2>Hello, {username}!</h2>
        <p><strong>Goal:</strong> {goal}</p>
        <p><strong>Intensity:</strong> {intensity}</p>
        <hr>
        <h2>Your Updated 7-Day Plan</h2>
        <pre>{plan}</pre>
        <hr>
        <h2>Give More Feedback</h2>
        <form action="/submit-feedback" method="post">
            <input type="hidden" name="user_id" value="{user_id}">
            <input type="hidden" name="username" value="{username}">
            <input type="hidden" name="goal" value="{goal}">
            <input type="hidden" name="intensity" value="{intensity}">
            <textarea name="old_plan" style="display:none;">{plan}</textarea>
            <label for="feedback">What would you like to change?</label>
            <textarea id="feedback" name="feedback" rows="5" required></textarea>
            <button type="submit">Update My Plan</button>
        </form>
        <p><a href="/">Create New Plan</a></p>
    """


app = FastAPI(title="FitBuddy AI")
app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.routes:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=False,
    )
