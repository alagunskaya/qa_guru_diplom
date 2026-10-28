def assert_status(response, expected_status):
    assert response.status_code == expected_status, (
        f"Ожидали {expected_status}, получили {response.status_code}. Тело: {response.text}")


def assert_json_content_type(response):
    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type, (
        f"Ожидали Content-Type: application/json, получили: {content_type}"
    )
