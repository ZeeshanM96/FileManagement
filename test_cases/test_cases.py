import pytest
from fastapi.testclient import TestClient
from app.apis import app

# Create a TestClient instance to send HTTP requests to your FastAPI app
client = TestClient(app)

def test_list_files():
    response = client.get("/list_files/files")
    assert response.status_code == 200
    assert "folder_name" in response.json()
    assert "files" in response.json()

def test_list_files_with_pagination():
    response = client.get("/list_files/files?count=5")
    assert response.status_code == 200
    assert "folder_name" in response.json()
    assert "files" in response.json()

def test_filter_files_by_name():
    response = client.get("/filter_files/files/BPmaWzuUWb")
    assert response.status_code == 200
    assert "folder_name" in response.json()
    assert "files" in response.json()

def test_order_files_by_size():
    response = client.get("/order_files_by_size/files")
    assert response.status_code == 200
    assert "folder_name" in response.json()
    assert "files" in response.json()

def test_filter_files_by_type():
    response = client.get("/filter_files_by_type/files/png")
    assert response.status_code == 200
    assert "folder_name" in response.json()
    assert "files" in response.json()

def test_invalid_count_parameter():
    response = client.get("/list_files/files?count=-1")
    assert response.status_code == 400


