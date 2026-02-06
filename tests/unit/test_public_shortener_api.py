from fastapi.testclient import TestClient


def test_shorten_returns_short_code_and_url(client: TestClient):
    """POST /v1/shorten возвращает short_code и short_url."""
    response = client.post(
        "/v1/shorten",
        json={"url": "https://example.com/page"},
    )
    assert response.status_code == 200
    data = response.json()

    assert "result" in data

    result = data["result"]

    assert "short_code" in result
    assert "short_url" in result
    assert len(result["short_code"]) >= 6
    assert result["short_url"].endswith(f"/v1/go/{result['short_code']}")


def test_shorten_same_url_returns_same_code(client: TestClient):
    """Одна и та же длинная ссылка возвращает один и тот же код"""
    url = "https://example.com/same"
    r1 = client.post("/v1/shorten", json={"url": url})
    r2 = client.post("/v1/shorten", json={"url": url})

    assert r1.status_code == 200 and r2.status_code == 200
    assert r1.json()["result"]["short_code"] == r2.json()["result"]["short_code"]


def test_redirect_by_code_returns_307_and_location(client: TestClient):
    """GET /v1/go/{code} возвращает 307 и редирект на длинную ссылку."""

    long_url = "https://example.com/redirect-here"

    create = client.post("/v1/shorten", json={"url": long_url})

    assert create.status_code == 200

    code = create.json()["result"]["short_code"]

    response = client.get(f"/v1/go/{code}", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == long_url


def test_redirect_unknown_code_returns_404(client: TestClient):
    """GET /v1/go/{code} для несуществующего кода возвращает 404."""
    response = client.get("/v1/go/nonexistent123")

    data = response.json()

    assert response.status_code == 404
    assert "error_message" in data
    assert "result" in data or "error_message" in data


def test_shorten_invalid_url_returns_422(client: TestClient):
    """POST /v1/shorten с невалидным URL возвращает 422."""
    response = client.post(
        "/v1/shorten",
        json={"url": "not-a-valid-url"},
    )
    assert response.status_code == 422
