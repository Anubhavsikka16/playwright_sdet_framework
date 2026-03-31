def test_auth_api(api_client):
    response = api_client.get("/user")
    assert response.status_code == 200