"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Competitive soccer training and matches",
        "schedule": "Mondays, Wednesdays, 4:00 PM - 6:00 PM",
        "max_participants": 22,
        "participants": ["alex@mergington.edu", "riley@mergington.edu"]
    },
    "Basketball Club": {
        "description": "Pickup games, drills, and intramural tournaments",
        "schedule": "Tuesdays and Thursdays, 4:30 PM - 6:00 PM",
        "max_participants": 18,
        "participants": ["tyler@mergington.edu", "madison@mergington.edu"]
    },
    "Art Club": {
        "description": "Drawing, painting, and mixed-media workshops",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["isabella@mergington.edu", "liam@mergington.edu"]
    },
    "Drama Club": {
        "description": "Theater production, acting exercises, and performances",
        "schedule": "Fridays, 4:00 PM - 6:00 PM",
        "max_participants": 25,
        "participants": ["ava@mergington.edu", "noah@mergington.edu"]
    },
    "Robotics Club": {
        "description": "Design and build robots for competitions and learning",
        "schedule": "Mondays and Thursdays, 5:00 PM - 7:00 PM",
        "max_participants": 12,
        "participants": ["oliver@mergington.edu", "charlotte@mergington.edu"]
    },
    "Debate Team": {
        "description": "Competitive debating and public speaking practice",
        "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
        "max_participants": 14,
        "participants": ["liam@mergington.edu", "emma@mergington.edu"]
    },

    # Sports (added)
    "Volleyball Team": {
        "description": "Team practices, drills, and inter-school matches",
        "schedule": "Wednesdays and Fridays, 4:30 PM - 6:00 PM",
        "max_participants": 20,
        "participants": ["nora@mergington.edu", "jack@mergington.edu"]
    },
    "Swimming Club": {
        "description": "Lap training, technique workshops, and friendly meets",
        "schedule": "Tuesdays and Thursdays, 5:00 PM - 6:30 PM",
        "max_participants": 24,
        "participants": ["sarah@mergington.edu", "matt@mergington.edu"]
    },

    # Artistic (added)
    "Photography Club": {
        "description": "Photo walks, editing sessions, and portfolio building",
        "schedule": "Mondays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["zoe@mergington.edu", "ben@mergington.edu"]
    },
    "Choir": {
        "description": "Vocal training, ensemble practice, and performances",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 30,
        "participants": ["grace@mergington.edu", "sam@mergington.edu"]
    },

    # Intellectual (added)
    "Math Club": {
        "description": "Problem solving, math competitions, and enrichment",
        "schedule": "Wednesdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["olivia@mergington.edu", "ethan@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Hands-on experiments, team challenges, and competitions",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["mia@mergington.edu", "dylan@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/participants")
def unregister_participant(activity_name: str, email: str):
    """Unregister a student (remove from participants) for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]

    if email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="Participant not found in activity")

    # Remove the student
    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}
