"""
Shared test fixtures and configuration for the Mergington High School API tests
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


# Original activities data to reset between tests
ORIGINAL_ACTIVITIES = {
    "Basketball": {
        "description": "Learn basketball skills and compete in games",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["james@mergington.edu"]
    },
    "Soccer": {
        "description": "Soccer practice and friendly matches",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["alex@mergington.edu"]
    },
    "Debate Club": {
        "description": "Develop argumentation and public speaking skills",
        "schedule": "Wednesdays, 3:30 PM - 4:30 PM",
        "max_participants": 16,
        "participants": ["lucas@mergington.edu"]
    },
    "Robotics Club": {
        "description": "Build and program robots for competitions",
        "schedule": "Saturdays, 10:00 AM - 12:00 PM",
        "max_participants": 10,
        "participants": ["ava@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act in theatrical productions and improve performance skills",
        "schedule": "Mondays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 25,
        "participants": ["isabella@mergington.edu"]
    },
    "Art Studio": {
        "description": "Learn painting, drawing, and sculpture techniques",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["mia@mergington.edu"]
    },
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
    }
}


@pytest.fixture
def test_client():
    """Fixture that provides a TestClient for the FastAPI app"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Fixture that resets activities to their original state before each test.
    Autouse=True ensures this runs before every test automatically.
    """
    # Reset to original data before each test
    activities.clear()
    activities.update(ORIGINAL_ACTIVITIES)
    
    yield
    
    # Cleanup after test (optional, but good practice)
    activities.clear()
    activities.update(ORIGINAL_ACTIVITIES)
