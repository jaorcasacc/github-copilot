"""
Tests for GET /activities endpoint
Using AAA (Arrange-Act-Assert) pattern
"""
import pytest


def test_get_activities_returns_all_activities(client, reset_activities):
    """Test that GET /activities returns all activities"""
    # ARRANGE
    expected_activity_count = 9
    expected_activity_names = [
        "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
        "Tennis Club", "Debate Club", "Science Olympiad", "Art Club", "Music Performance"
    ]
    
    # ACT
    response = client.get("/activities")
    
    # ASSERT
    assert response.status_code == 200
    activities = response.json()
    assert len(activities) == expected_activity_count
    assert all(name in activities for name in expected_activity_names)


def test_get_activities_returns_correct_structure(client, reset_activities):
    """Test that each activity has required fields"""
    # ARRANGE
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    # ACT
    response = client.get("/activities")
    activities = response.json()
    
    # ASSERT
    assert response.status_code == 200
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_data, dict)
        assert all(field in activity_data for field in required_fields)
        assert isinstance(activity_data["participants"], list)
        assert isinstance(activity_data["max_participants"], int)


def test_get_activities_participants_are_list_of_strings(client, reset_activities):
    """Test that participants are stored as list of email strings"""
    # ARRANGE
    activity_name = "Chess Club"
    
    # ACT
    response = client.get("/activities")
    activities = response.json()
    
    # ASSERT
    assert response.status_code == 200
    participants = activities[activity_name]["participants"]
    assert isinstance(participants, list)
    assert all(isinstance(email, str) for email in participants)
    assert len(participants) > 0


def test_get_activities_max_participants_is_positive_integer(client, reset_activities):
    """Test that max_participants field contains valid positive integers"""
    # ARRANGE
    
    # ACT
    response = client.get("/activities")
    activities = response.json()
    
    # ASSERT
    assert response.status_code == 200
    for activity_data in activities.values():
        assert activity_data["max_participants"] > 0
        assert isinstance(activity_data["max_participants"], int)
