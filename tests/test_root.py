"""
Tests for GET / endpoint
Using AAA (Arrange-Act-Assert) pattern
"""
import pytest


def test_root_redirects_to_index(client, reset_activities):
    """Test that root path redirects to /static/index.html"""
    # ARRANGE
    expected_redirect_location = "/static/index.html"
    
    # ACT
    response = client.get("/", follow_redirects=False)
    
    # ASSERT
    assert response.status_code == 307
    assert response.headers["location"] == expected_redirect_location


def test_root_with_redirect_follows_to_static(client, reset_activities):
    """Test that root path successfully redirects and loads static content"""
    # ARRANGE
    
    # ACT
    response = client.get("/", follow_redirects=True)
    
    # ASSERT
    assert response.status_code == 200
    assert "<!doctype html>" in response.text.lower()
    assert "mergington" in response.text.lower()
