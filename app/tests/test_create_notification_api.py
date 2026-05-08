import pytest
from unittest.mock import MagicMock, patch
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


def test_create_notification_success(client):
    '''
    Тестирует успешное создания уведомлений.  
    '''
    payload = {
        "type": "email",
        "recipient": "test@example.com",
        "subject": "Hello",
        "message": "World",
        "channel_data": {"provider": "sendgrid"}
    }
    
    mock_notif = MagicMock()
    mock_notif.id = "550e8400-e29b-41d4-a716-446655440000"
    mock_notif.status = NotificationStatus.QUEUED

    with patch('notification_repository.NotificationRepository.create', return_value=mock_notif), \
         patch('main.send_notification_task.delay') as mock_task:
        
        response = client.post('/api/v1/notifications', json=payload)
        
        assert response.status_code == 201
        assert response.json['id'] == mock_notif.id
        mock_task.assert_called_once_with(str(mock_notif.id))

def test_create_notification_validation_error(client):
    '''
    Тестирует появление ошибки при отправки не полного JSON.
    '''
    incomplete_payload = {
        "type": "email",
        "message": "Missing recipient"
    }
    
    response = client.post('/api/v1/notifications', json=incomplete_payload)
    
    assert response.status_code == 400
    assert any(err['loc'] == ['recipient'] for err in response.json)

def test_create_notification_invalid_json(client):
    '''
    Тестирует появление ошибки при отправке не JSON формата.
    '''
    response = client.post(
        '/api/v1/notifications', 
        data="не json формат", 
        content_type='application/json'
    )
    
    assert response.status_code == 400


def test_create_notification_triggers_task_with_string_id(client):
    '''
    Тестирует вызов отправки уведомления при создании уведомления.
    '''
    payload = {
        "type": "sms",
        "recipient": "+79991234567",
        "message": "Code: 1234"
    }
    
    import uuid
    generated_id = uuid.uuid4()
    mock_notif = MagicMock()
    mock_notif.id = generated_id
    mock_notif.status = "queued"

    with patch('notification_repository.NotificationRepository.create', return_value=mock_notif), \
         patch('main.send_notification_task.delay') as mock_task:
        
        response = client.post('/api/v1/notifications', json=payload)
        
        assert response.status_code == 201
        mock_task.assert_called_once_with(str(generated_id))