"""
Tests for POST /activities/{activity_name}/signup endpoint
Using AAA (Arrange-Act-Assert) pattern
"""
import pytest


def test_signup_successful_adds_participant(client, reset_activities):
    """Test that successful signup adds participant to activity"""
    # ARRANGE
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    initial_count = len(client.get("/activities").json()[activity_name]["participants"])
    
    # ACT
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # ASSERT
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    
    # Verify participant was added
    updated_activities = client.get("/activities").json()
    assert email in updated_activities[activity_name]["participants"]
    assert len(updated_activities[activity_name]["participants"]) == initial_count + 1


def test_signup_nonexistent_activity_returns_404(client, reset_activities):
    """Test that signup for non-existent activity returns 404"""
    # ARRANGE
    activity_name = "Nonexistent Activity"
    email = "student@mergington.edu"
    
    # ACT
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # ASSERT
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_email_returns_400(client, reset_activities):
    """Test that duplicate signup returns 400 error"""
    # ARRANGE
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already registered
    
    # ACT
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # ASSERT
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_first_time_email_succeeds(client, reset_activities):
    """Test that same email can sign up for different activity"""
    # ARRANGE
    first_activity = "Chess Club"
    second_activity = "Programming Class"
    email = "student@mergington.edu"
    
    # ACT - Sign up for first activity
    response1 = client.post(f"/activities/{first_activity}/signup?email={email}")
    
    # ASSERT - First signup successful
    assert response1.status_code == 200
    
    # ACT - Sign up for second activity
    response2 = client.post(f"/activities/{second_activity}/signup?email={email}")
    
    # ASSERT - Second signup successful
    assert response2.status_code == 200
    activities = client.get("/activities").json()
    assert email in activities[first_activity]["participants"]
    assert email in activities[second_activity]["participants"]


def test_signup_with_special_characters_in_email(client, reset_activities):
    """Test signup with special characters in email"""
    # ARRANGE
    activity_name = "Chess Club"
    email = "student+tag@mergington.edu"
    
    # ACT
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    
    # ASSERT
    assert response.status_code == 200
    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]


def test_signup_returns_message(client, reset_activities):
    """Test that signup returns appropriate success message"""
    # ARRANGE
    activity_name = "Tennis Club"
    email = "player@mergington.edu"
    
    # ACT
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    result = response.json()
    
    # ASSERT
    assert response.status_code == 200
    assert "message" in result
    assert email in result["message"]
    assert activity_name in result["message"]


def test_signup_second_attempt_same_email_same_activity_fails(client, reset_activities):
    """Test that attempting to signup twice for same activity fails"""
    # ARRANGE
    activity_name = "Debate Club"
    email = "debater@mergington.edu"
    
    # ACT - First signup
    response1 = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response1.status_code == 200
    
    # ACT - Try second signup
    response2 = client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # ASSERT
    assert response2.status_code == 400
    assert "already signed up" in response2.json()["detail"]
