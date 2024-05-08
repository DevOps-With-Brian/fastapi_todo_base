from ..main import app
from fastapi import status
import sys
import os
from .utils import client

# Get the parent directory of the current file (assuming test_main.py is in TodoApp/tests)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the parent directory to sys.path
sys.path.insert(0, parent_dir)


def test_return_health_check():
    response = client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'Healthy'}
