"""
Tests for DELETE /activities/{activity_name}/signup endpoint
Using AAA (Arrange-Act-Assert) pattern
"""
import pytest


def test_remove_successful_deletes_participant(client, reset_activities):
    """Test that DELETE successfully removes a participant"""
    # ARRANGE
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already registered
    initial_count = len(client.get("/activities").json()[activity_name]["participants"])
    
    # ACT
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")
    
    # ASSERT
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"
    
    # Verify participant was removed
    updated_activities = client.get("/activities").json()
    assert email not in updated_activities[activity_name]["participants"]
    assert len(updated_activities[activity_name]["participants"]) == initial_count - 1


def test_remove_nonexistent_activity_returns_404(client, reset_activities):
    """Test that remove from non-existent activity returns 404"""
    # ARRANGE
    activity_name = "Nonexistent Activity"
    email = "student@mergington.edu"
    
    # ACT
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")
    
    # ASSERT
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_unregistered_participant_returns_400(client, reset_activities):
    """Test that removing unregistered participant returns 400"""
    # ARRANGE
    activity_name = "Chess Club"
    email = "notregistered@mergington.edu"  # Not in participants list
    
    # ACT
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")
    
    # ASSERT
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]


def test_remove_then_resignup_succeeds(client, reset_activities):
    """Test that a student can re-register after being removed"""
    # ARRANGE
    activity_name = "Programming Class"
    email = "emma@mergington.edu"
    
    # ACT - Remove participant
    response1 = client.delete(f"/activities/{activity_name}/signup?email={email}")
    assert response1.status_code == 200
    
    # Verify removal
    activities_after_remove = client.get("/activities").json()
    assert email not in activities_after_remove[activity_name]["participants"]
    
    # ACT - Re-register
    response2 = client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # ASSERT
    assert response2.status_code == 200
    activities_after_signup = client.get("/activities").json()
    assert email in activities_after_signup[activity_name]["participants"]


def test_remove_returns_message(client, reset_activities):
    """Test that remove returns appropriate success message"""
    # ARRANGE
    activity_name = "Tennis Club"
    email = "alex@mergington.edu"
    
    # ACT
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")
    result = response.json()
    
    # ASSERT
    assert response.status_code == 200
    assert "message" in result
    assert email in result["message"]
    assert activity_name in result["message"]


def test_remove_second_attempt_same_participant_fails(client, reset_activities):
    """Test that attempting to remove twice fails"""
    # ARRANGE
    activity_name = "Science Olympiad"
    email = "noah@mergington.edu"
    
    # ACT - First removal
    response1 = client.delete(f"/activities/{activity_name}/signup?email={email}")
    assert response1.status_code == 200
    
    # ACT - Try second removal
    response2 = client.delete(f"/activities/{activity_name}/signup?email={email}")
    
    # ASSERT
    assert response2.status_code == 400
    assert "not signed up" in response2.json()["detail"]


def test_remove_does_not_affect_other_participants(client, reset_activities):
    """Test that removing one participant doesn't affect others"""
    # ARRANGE
    activity_name = "Chess Club"
    email_to_remove = "michael@mergington.edu"
    email_to_keep = "daniel@mergington.edu"
    
    # ACT
    response = client.delete(f"/activities/{activity_name}/signup?email={email_to_remove}")
    
    # ASSERT
    assert response.status_code == 200
    updated_activities = client.get("/activities").json()
    assert email_to_remove not in updated_activities[activity_name]["participants"]
    assert email_to_keep in updated_activities[activity_name]["participants"]
