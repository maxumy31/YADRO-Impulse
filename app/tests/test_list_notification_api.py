from dataclasses import dataclass

import pytest
from unittest.mock import MagicMock, patch
import uuid
from main import app as flask_app
from notification_repository import NotificationRepository
from model import *


@pytest.fixture
def app():
    flask_app.config.update({"TESTING": True})
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def mock_db():
    return MagicMock(spec=NotificationRepository)

@dataclass
class FakeNotification:
    id: str
    status: NotificationStatus
    error_text: str = None

def test_list_notifications_defaults_empty(client):
    with patch('notification_repository.NotificationRepository.get_list', return_value=[]) as mock_get:
        response = client.get('/api/v1/notifications')
        
        assert response.status_code == 200
        assert response.json == []
        mock_get.assert_called_once_with(10, 0, None)

def test_list_notifications_defaults(client):
    fake_count = 10
    fake_data = [
        FakeNotification(id=str(uuid.uuid4()), status=NotificationStatus.SENT)
        for i in range(fake_count)
    ]

    with patch('notification_repository.NotificationRepository.get_list', return_value=fake_data) as mock_get:
        response = client.get('/api/v1/notifications')
        
        assert response.status_code == 200
        assert len(response.json) == fake_count
        mock_get.assert_called_once_with(10, 0, None)

def test_list_notifications_with_params(client):
    fake_data = [
        FakeNotification(id="a1ede6a7-050f-4f4a-9f11-2ae2dc69c3ab", status=NotificationStatus.SENT),
        FakeNotification(id="4a8becce-254e-4f1a-822c-db15c892ffbe", status=NotificationStatus.QUEUED)
    ]
    
    with patch('notification_repository.NotificationRepository.get_list') as mock_get:
        mock_get.return_value = fake_data
        
        response = client.get('/api/v1/notifications?limit=5&offset=10&status=sent')
        
        assert response.status_code == 200
        assert len(response.json) == 2
        assert response.json[0]['id'] == "a1ede6a7-050f-4f4a-9f11-2ae2dc69c3ab"
        assert response.json[1]['id'] == "4a8becce-254e-4f1a-822c-db15c892ffbe"
        
        mock_get.assert_called_once_with(5, 10, "sent")

def test_list_notifications_invalid_params(client):
    response = client.get('/api/v1/notifications?limit=abc')
    
    assert response.status_code == 400
    
    errors = response.json

    assert any(err['loc'] == ['limit'] for err in errors)
