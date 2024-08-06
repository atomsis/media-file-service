from fastapi.testclient import TestClient
from app.main import app
import os
import pytest

client = TestClient(app)

def create_test_file(file_path: str, content: bytes):
    """Helper function to create a test file."""
    with open(file_path, 'wb') as f:
        f.write(content)

def delete_test_file(file_path: str):
    """Helper function to delete a test file if it exists."""
    if os.path.exists(file_path):
        os.remove(file_path)

def test_upload_file():
    """
    Test the file upload functionality.
    """
    test_file_path = './test_upload.jpg'
    create_test_file(test_file_path, b"test file content")

    with open(test_file_path, 'rb') as f:
        response = client.post("/upload", files={"file": f})

    assert response.status_code == 200
    assert "uid" in response.json()

    delete_test_file(test_file_path)

def test_download_file():
    """
    Test the file download functionality using the UID obtained after upload.
    """
    test_file_path = './test_upload.jpg'
    create_test_file(test_file_path, b"test file content")

    with open(test_file_path, 'rb') as f:
        response = client.post("/upload", files={"file": f})

    uid = response.json().get("uid")
    download_url = f"/file/{uid}"

    download_response = client.get(download_url)

    assert download_response.status_code == 200
    assert download_response.content == b'{"filename":"test_upload.jpg","file_path":"./uploads/test_upload.jpg"}'

    delete_test_file(test_file_path)
