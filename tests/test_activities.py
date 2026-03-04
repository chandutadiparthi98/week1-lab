"""
Tests for the GET /activities endpoint using AAA (Arrange-Act-Assert) pattern
"""

import pytest


class TestGetActivities:
    """Test suite for GET /activities endpoint"""

    def test_get_activities_returns_status_200(self, test_client):
        """
        Test that GET /activities returns a successful 200 status code
        
        Arrange: Test client is ready (provided by fixture)
        Act: Make GET request to /activities
        Assert: Response status code is 200
        """
        # Arrange
        expected_status_code = 200
        
        # Act
        response = test_client.get("/activities")
        
        # Assert
        assert response.status_code == expected_status_code

    def test_get_activities_returns_all_activities(self, test_client):
        """
        Test that GET /activities returns all 9 pre-populated activities
        
        Arrange: Test client is ready
        Act: Make GET request to /activities
        Assert: Response contains all 9 activities
        """
        # Arrange
        expected_activity_count = 9
        expected_activity_names = {
            "Basketball", "Soccer", "Debate Club", "Robotics Club",
            "Drama Club", "Art Studio", "Chess Club", "Programming Class",
            "Gym Class"
        }
        
        # Act
        response = test_client.get("/activities")
        activities = response.json()
        
        # Assert
        assert len(activities) == expected_activity_count
        assert set(activities.keys()) == expected_activity_names

    def test_get_activities_has_correct_structure(self, test_client):
        """
        Test that each activity has the required fields with correct types
        
        Arrange: Expected structure for an activity object
        Act: Make GET request to /activities
        Assert: Each activity has description, schedule, max_participants, and participants
        """
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = test_client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data, dict), f"{activity_name} should be a dict"
            assert set(activity_data.keys()) == required_fields, f"{activity_name} missing required fields"
            assert isinstance(activity_data["description"], str), f"{activity_name} description should be string"
            assert isinstance(activity_data["schedule"], str), f"{activity_name} schedule should be string"
            assert isinstance(activity_data["max_participants"], int), f"{activity_name} max_participants should be int"
            assert isinstance(activity_data["participants"], list), f"{activity_name} participants should be list"

    def test_get_activities_participants_are_strings(self, test_client):
        """
        Test that all participants in the participants list are strings (emails)
        
        Arrange: Test client is ready
        Act: Make GET request to /activities
        Assert: All participants are strings
        """
        # Arrange
        # No special arrangement needed
        
        # Act
        response = test_client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity_name, activity_data in activities.items():
            for participant in activity_data["participants"]:
                assert isinstance(participant, str), f"{activity_name} has non-string participant: {participant}"

    def test_get_activities_valid_response_json(self, test_client):
        """
        Test that GET /activities returns valid JSON and is not empty
        
        Arrange: Test client is ready
        Act: Make GET request to /activities
        Assert: Response is valid JSON dict and not empty
        """
        # Arrange
        # No special arrangement needed
        
        # Act
        response = test_client.get("/activities")
        activities = response.json()
        
        # Assert
        assert isinstance(activities, dict)
        assert len(activities) > 0
