"""
Tests for the Mergington High School Activities API

Using AAA (Arrange-Act-Assert) pattern for clear test structure.
"""


class TestGetActivities:
    """Tests for GET /activities endpoint"""
    
    def test_get_all_activities(self, client):
        """Test that we can retrieve all activities"""
        # Arrange
        # (No setup needed for this test)
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) > 0
        assert "Chess Club" in data
        assert "Programming Class" in data
    
    def test_activity_has_required_fields(self, client):
        """Test that each activity has all required fields"""
        # Arrange
        # (No setup needed for this test)
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity_name, activity_data in data.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_for_activity(self, client):
        """Test successful signup for an activity"""
        # Arrange
        email = "test.student@mergington.edu"
        
        # Act
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
    
    def test_signup_duplicate_email(self, client):
        """Test that duplicate signup is rejected"""
        # Arrange
        email = "michael@mergington.edu"  # Already in Chess Club
        
        # Act
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
    
    def test_signup_nonexistent_activity(self, client):
        """Test signup for activity that doesn't exist"""
        # Arrange
        email = "test.student@mergington.edu"
        
        # Act
        response = client.post(
            "/activities/Nonexistent Activity/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]


class TestRemoveParticipant:
    """Tests for DELETE /activities/{activity_name}/participants/{email} endpoint"""
    
    def test_remove_participant(self, client):
        """Test successful removal of a participant"""
        # Arrange
        email = "michael@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/Chess Club/participants/{email}"
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
    
    def test_remove_nonexistent_participant(self, client):
        """Test removal of participant who isn't signed up"""
        # Arrange
        email = "nonexistent@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/Chess Club/participants/{email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
    
    def test_remove_from_nonexistent_activity(self, client):
        """Test removal from activity that doesn't exist"""
        # Arrange
        email = "test@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/Nonexistent Activity/participants/{email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
