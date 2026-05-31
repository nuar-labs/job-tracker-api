from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.api.deps import get_db
from app.db.base import Base
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


client = TestClient(app)


def create_user_and_token(email="test@example.com", password="password123"):
    client.post(
        "/auth/register",
        json={"email": email, "password": password},
    )
    login_response = client.post(
        "/auth/login",
        data={"username": email, "password": password},
    )
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_job():
    headers = create_user_and_token()

    response = client.post(
        "/jobs",
        json={
            "company": "Google",
            "role": "Backend Engineer",
            "link": "https://example.com/job",
            "status": "applied",
            "notes": "first test",
        },
        headers=headers,
    )

    assert response.status_code == 201
    data = response.json()
    assert data["company"] == "Google"
    assert data["role"] == "Backend Engineer"
    assert data["status"] == "applied"
    assert "id" in data


def test_list_jobs():
    headers = create_user_and_token()

    client.post(
        "/jobs",
        json={
            "company": "Google",
            "role": "Backend Engineer",
            "link": "https://example.com/job",
            "status": "applied",
            "notes": "first test",
        },
        headers=headers,
    )

    response = client.get("/jobs", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["company"] == "Google"


def test_get_job():
    headers = create_user_and_token()

    create_response = client.post(
        "/jobs",
        json={
            "company": "Google",
            "role": "Backend Engineer",
            "link": "https://example.com/job",
            "status": "applied",
            "notes": "first test",
        },
        headers=headers,
    )
    job_id = create_response.json()["id"]

    response = client.get(f"/jobs/{job_id}", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == job_id
    assert data["company"] == "Google"


def test_update_job():
    headers = create_user_and_token()

    create_response = client.post(
        "/jobs",
        json={
            "company": "Google",
            "role": "Backend Engineer",
            "link": "https://example.com/job",
            "status": "applied",
            "notes": "first test",
        },
        headers=headers,
    )
    job_id = create_response.json()["id"]

    response = client.patch(
        f"/jobs/{job_id}",
        json={"status": "interview", "notes": "updated"},
        headers=headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "interview"
    assert data["notes"] == "updated"


def test_delete_job():
    headers = create_user_and_token()

    create_response = client.post(
        "/jobs",
        json={
            "company": "Google",
            "role": "Backend Engineer",
            "link": "https://example.com/job",
            "status": "applied",
            "notes": "first test",
        },
        headers=headers,
    )
    job_id = create_response.json()["id"]

    delete_response = client.delete(f"/jobs/{job_id}", headers=headers)
    assert delete_response.status_code == 204

    get_response = client.get(f"/jobs/{job_id}", headers=headers)
    assert get_response.status_code == 404