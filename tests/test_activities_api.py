def test_get_activities_returns_available_activities(client):
    # Arrange
    endpoint = "/activities"

    # Act
    response = client.get(endpoint)

    # Assert
    assert response.status_code == 200
    assert "Chess Club" in response.json()


def test_signup_adds_participant(client):
    # Arrange
    activity = "Soccer Team"
    email = "student@example.com"

    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert email in client.get("/activities").json()[activity]["participants"]


def test_signup_rejects_duplicate_participant(client):
    # Arrange
    activity = "Soccer Team"
    email = "student@example.com"
    client.post(f"/activities/{activity}/signup", params={"email": email})

    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_signup_rejects_unknown_activity(client):
    # Arrange
    activity = "Unknown Activity"

    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": "student@example.com"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_removes_participant(client):
    # Arrange
    activity = "Soccer Team"
    email = "student@example.com"
    client.post(f"/activities/{activity}/signup", params={"email": email})

    # Act
    response = client.delete(
        f"/activities/{activity}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert email not in client.get("/activities").json()[activity]["participants"]


def test_unregister_rejects_unregistered_participant(client):
    # Arrange
    activity = "Soccer Team"

    # Act
    response = client.delete(
        f"/activities/{activity}/signup",
        params={"email": "student@example.com"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_rejects_unknown_activity(client):
    # Arrange
    activity = "Unknown Activity"

    # Act
    response = client.delete(
        f"/activities/{activity}/signup",
        params={"email": "student@example.com"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"