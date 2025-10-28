"""
Test suite for the Mergington High School Activities API
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities data before each test"""
    # Store original data
    original_activities = {
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
            "description": "Competitive soccer training and inter-school matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 25,
            "participants": ["alex@mergington.edu", "sarah@mergington.edu"]
        },
        "Swimming Club": {
            "description": "Swimming techniques and competitive swimming events",
            "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participants": ["james@mergington.edu"]
        },
        "Art Studio": {
            "description": "Painting, drawing, and mixed media art projects",
            "schedule": "Fridays, 2:00 PM - 4:00 PM",
            "max_participants": 18,
            "participants": ["lily@mergington.edu", "grace@mergington.edu"]
        },
        "Drama Club": {
            "description": "Acting, theater production, and performance arts",
            "schedule": "Wednesdays and Fridays, 3:30 PM - 5:30 PM",
            "max_participants": 20,
            "participants": ["noah@mergington.edu", "isabella@mergington.edu", "ethan@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop critical thinking and public speaking through competitive debates",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["ava@mergington.edu", "william@mergington.edu"]
        },
        "Science Olympiad": {
            "description": "Competitive science events covering biology, chemistry, physics, and engineering",
            "schedule": "Tuesdays, 3:30 PM - 5:30 PM",
            "max_participants": 24,
            "participants": ["mia@mergington.edu", "benjamin@mergington.edu", "charlotte@mergington.edu"]
        }
    }
    
    # Reset activities to original state
    activities.clear()
    activities.update(original_activities)
    yield
    # Cleanup after test
    activities.clear()
    activities.update(original_activities)


class TestRootEndpoint:
    """Test the root endpoint redirect"""
    
    def test_root_redirects_to_static_index(self, client):
        """Test that root path redirects to static index.html"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


class TestGetActivities:
    """Test the get activities endpoint"""
    
    def test_get_all_activities_success(self, client, reset_activities):
        """Test successful retrieval of all activities"""
        response = client.get("/activities")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == 9  # Should have 9 activities
        
        # Check that specific activities exist
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Soccer Team" in data
        
        # Verify structure of an activity
        chess_club = data["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)
    
    def test_get_activities_includes_all_fields(self, client, reset_activities):
        """Test that all required fields are present in activity data"""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_data in data.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["max_participants"], int)
            assert isinstance(activity_data["participants"], list)


class TestSignupForActivity:
    """Test the signup for activity endpoint"""
    
    def test_signup_success(self, client, reset_activities):
        """Test successful signup for an activity"""
        response = client.post(
            "/activities/Chess Club/signup?email=newstudent@mergington.edu"
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "newstudent@mergington.edu" in data["message"]
        assert "Chess Club" in data["message"]
        
        # Verify the participant was actually added
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert "newstudent@mergington.edu" in activities_data["Chess Club"]["participants"]
    
    def test_signup_activity_not_found(self, client, reset_activities):
        """Test signup for non-existent activity"""
        response = client.post(
            "/activities/Nonexistent Activity/signup?email=student@mergington.edu"
        )
        assert response.status_code == 404
        
        data = response.json()
        assert data["detail"] == "Activity not found"
    
    def test_signup_duplicate_registration(self, client, reset_activities):
        """Test that duplicate registrations are prevented"""
        # First signup should succeed
        response1 = client.post(
            "/activities/Chess Club/signup?email=newstudent@mergington.edu"
        )
        assert response1.status_code == 200
        
        # Second signup should fail
        response2 = client.post(
            "/activities/Chess Club/signup?email=newstudent@mergington.edu"
        )
        assert response2.status_code == 400
        
        data = response2.json()
        assert "already signed up" in data["detail"]
    
    def test_signup_existing_participant_duplicate(self, client, reset_activities):
        """Test that existing participants can't sign up again"""
        # Try to signup with an email that's already in the activity
        response = client.post(
            "/activities/Chess Club/signup?email=michael@mergington.edu"
        )
        assert response.status_code == 400
        
        data = response.json()
        assert "already signed up" in data["detail"]
    
    def test_signup_with_url_encoded_activity_name(self, client, reset_activities):
        """Test signup with URL encoded activity name"""
        response = client.post(
            "/activities/Art%20Studio/signup?email=newartist@mergington.edu"
        )
        assert response.status_code == 200
        
        # Verify the participant was added
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert "newartist@mergington.edu" in activities_data["Art Studio"]["participants"]


class TestUnregisterFromActivity:
    """Test the unregister from activity endpoint"""
    
    def test_unregister_success(self, client, reset_activities):
        """Test successful unregistration from an activity"""
        # First, verify the participant is registered
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert "michael@mergington.edu" in activities_data["Chess Club"]["participants"]
        
        # Unregister the participant
        response = client.delete(
            "/activities/Chess Club/unregister?email=michael@mergington.edu"
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "michael@mergington.edu" in data["message"]
        assert "Chess Club" in data["message"]
        
        # Verify the participant was actually removed
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert "michael@mergington.edu" not in activities_data["Chess Club"]["participants"]
    
    def test_unregister_activity_not_found(self, client, reset_activities):
        """Test unregister from non-existent activity"""
        response = client.delete(
            "/activities/Nonexistent Activity/unregister?email=student@mergington.edu"
        )
        assert response.status_code == 404
        
        data = response.json()
        assert data["detail"] == "Activity not found"
    
    def test_unregister_participant_not_registered(self, client, reset_activities):
        """Test unregister participant who is not registered"""
        response = client.delete(
            "/activities/Chess Club/unregister?email=notregistered@mergington.edu"
        )
        assert response.status_code == 400
        
        data = response.json()
        assert "not registered" in data["detail"]
    
    def test_unregister_with_url_encoded_activity_name(self, client, reset_activities):
        """Test unregister with URL encoded activity name"""
        response = client.delete(
            "/activities/Art%20Studio/unregister?email=lily@mergington.edu"
        )
        assert response.status_code == 200
        
        # Verify the participant was removed
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert "lily@mergington.edu" not in activities_data["Art Studio"]["participants"]


class TestEndToEndWorkflow:
    """Test complete workflows combining multiple operations"""
    
    def test_signup_and_unregister_workflow(self, client, reset_activities):
        """Test complete signup and unregister workflow"""
        test_email = "testworkflow@mergington.edu"
        activity_name = "Swimming Club"
        
        # Get initial participant count
        initial_response = client.get("/activities")
        initial_data = initial_response.json()
        initial_count = len(initial_data[activity_name]["participants"])
        
        # Sign up
        signup_response = client.post(
            f"/activities/{activity_name}/signup?email={test_email}"
        )
        assert signup_response.status_code == 200
        
        # Verify signup worked
        after_signup_response = client.get("/activities")
        after_signup_data = after_signup_response.json()
        assert test_email in after_signup_data[activity_name]["participants"]
        assert len(after_signup_data[activity_name]["participants"]) == initial_count + 1
        
        # Unregister
        unregister_response = client.delete(
            f"/activities/{activity_name}/unregister?email={test_email}"
        )
        assert unregister_response.status_code == 200
        
        # Verify unregister worked
        final_response = client.get("/activities")
        final_data = final_response.json()
        assert test_email not in final_data[activity_name]["participants"]
        assert len(final_data[activity_name]["participants"]) == initial_count
    
    def test_multiple_participants_different_activities(self, client, reset_activities):
        """Test multiple participants signing up for different activities"""
        test_participants = [
            ("student1@mergington.edu", "Chess Club"),
            ("student2@mergington.edu", "Programming Class"),
            ("student3@mergington.edu", "Soccer Team"),
        ]
        
        # Sign up all participants
        for email, activity in test_participants:
            response = client.post(f"/activities/{activity}/signup?email={email}")
            assert response.status_code == 200
        
        # Verify all participants are registered
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        
        for email, activity in test_participants:
            assert email in activities_data[activity]["participants"]


class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_invalid_activity_name_characters(self, client, reset_activities):
        """Test handling of special characters in activity names"""
        response = client.post(
            "/activities/Invalid<>Activity/signup?email=test@mergington.edu"
        )
        assert response.status_code == 404
    
    def test_empty_email_parameter(self, client, reset_activities):
        """Test handling of empty email parameter"""
        response = client.post("/activities/Chess Club/signup?email=")
        # This should still process, but with an empty email
        # The endpoint doesn't validate email format, just checks for duplicates
        assert response.status_code == 200
    
    def test_missing_email_parameter(self, client, reset_activities):
        """Test handling of missing email parameter"""
        response = client.post("/activities/Chess Club/signup")
        # FastAPI will return 422 for missing required query parameter
        assert response.status_code == 422


if __name__ == "__main__":
    pytest.main([__file__])