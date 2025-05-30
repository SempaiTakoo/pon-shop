import pytest

from fastapi.testclient import TestClient

from services.user_service.old_app.main import app


client = TestClient(app)
