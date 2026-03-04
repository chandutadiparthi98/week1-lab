"""
Tests for the POST /activities/{activity_name}/signup endpoint using AAA (Arrange-Act-Assert) pattern
"""

import pytest


class TestSignupForActivity:
    """Test suite for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_successful_returns_status_200(self, test_client):
        """
        Test that successful signup returns 200 status code
        
        Arrange: Valid activity name and email that hasn't signed up
        Act: POST signup request
        Assert: Response status code is 200
        """
        # Arrange
        activity_name = "Basketball"
        email = "newstudent@mergington.edu"
        expected_status_code = 200
        
        # Act
        response = test_client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == expected_status_code

    def test_signup_successful_returns_success_message(self, test_client):
        """
        Test that successful signup returns the correct success message
        
        Arrange: Valid activity name and email
        Act: POST signup request
        Assert: Response contains success message with correct email and activity
        """
        # Arrange
        activity_name = "Soccer"
        email = "student@mergington.edu"
        
        # Act
        response = test_client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        result = response.json()
        
        # Assert
        assert "message" in result
        assert email in result["message"]
        assert activity_name in result["message"]

    def test_signup_adds_email_to_participants(self, test_client):
        """
        Test that successful signup adds the email to the activity's participants list
        
        Arrange: Valid activity and email
        Act: POST signup request, then GET activities to verify
        Assert: Email is in the participants list for that activity
        """
        # Arrange
        activity_name = "Drama Club"
        email = "drama_student@mergington.edu"
        
        # Act
        response = test_client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        activities_response = test_client.get("/activities")
        activities = activities_response.json()
        
        # Assert
        assert response.status_code == 200
        assert email in activities[activity_name]["participants"]

    def test_signup_invalid_activity_returns_404(self, test_client):
        """
        Test that signup to a non-existent activity returns 404 status code
        
        Arrange: Invalid activity name and valid email
        Act: POST signup request
        Assert: Response status code is 404
        """
        # Arrange
        activity_name = "NonExistentActivity"
        email = "student@mergington.edu"
        expected_status_code = 404
        
        # Act
        response = test_client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == expected_status_code

    def test_signup_invalid_activity_returns_error_message(self, test_client):
        """
        Test that signup to a non-existent activity returns error detail
        
        Arrange: Invalid activity name
        Act: POST signup request
        Assert: Response contains "Activity not found" error message
        """
        # Arrange
        activity_name = "FakeActivity"
        email = "student@mergington.edu"
        
        # Act
        response = test_client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        result = response.json()
        
        # Assert
        assert "detail" in result
        assert "Activity not found" in result["detail"]

    def test_signup_with_special_characters_in_email(self, test_client):
        """
        Test that signup works with emails containing special characters
        
        Arrange: Valid activity and email with special characters
        Act: POST signup request
        Assert: Signup succeeds and email is stored correctly
        """
        # Arrange
        activity_name = "Art Studio"
        email = "student+special@mergington.edu"
        
        # Act
        response = test_client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        activities_response = test_client.get("/activities")
        activities = activities_response.json()
        
        # Assert
        assert response.status_code == 200
        assert email in activities[activity_name]["participants"]

    def test_signup_multiple_students_same_activity(self, test_client):
        """
        Test that multiple students can sign up for the same activity
        
        Arrange: Two different emails for the same activity
        Act: POST signup requests for both emails
        Assert: Both emails are in the participants list
        """
        # Arrange
        activity_name = "Chess Club"
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"
        
        # Act
        response1 = test_client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email1}
        )
        response2 = test_client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email2}
        )
        activities_response = test_client.get("/activities")
        activities = activities_response.json()
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert email1 in activities[activity_name]["participants"]
        assert email2 in activities[activity_name]["participants"]

    def test_signup_case_sensitive_activity_names(self, test_client):
        """
        Test that activity names are case-sensitive for signup
        
        Arrange: Correct case activity name vs incorrect case
        Act: POST signup with correct case (should succeed), then incorrect case (should fail)
        Assert: First succeeds, second fails with 404
        """
        # Arrange
        activity_correct = "Basketball"
        activity_incorrect = "basketball"
        email = "student@mergington.edu"
        
        # Act - correct case should work
        response_correct = test_client.post(
            f"/activities/{activity_correct}/signup",
            params={"email": email}
        )
        
        # Act - incorrect case should fail
        response_incorrect = test_client.post(
            f"/activities/{activity_incorrect}/signup",
            params={"email": email + "2"}
        )
        
        # Assert
        assert response_correct.status_code == 200
        assert response_incorrect.status_code == 404
