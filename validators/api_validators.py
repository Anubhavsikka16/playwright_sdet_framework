def validate_login_response(response):
    assert response.status_code == 200
    assert "token" in response.json()