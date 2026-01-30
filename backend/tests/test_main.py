def test_root(client):
    """Test the root endpoint returns API info."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "EAV CMS API"
    assert data["docs"] == "/docs"
