import uuid
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify, Flask, current_app
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from DTO.notificationDTO import (
    NotificationCreate, 
    NotificationCreateResponse,
    NotificationReadResponse,
    NotificationFilter
)
import logging
import sys
from model import *
from init import run_migrations
from functools import wraps
import json
from flask_injector import FlaskInjector
from injector import Binder, singleton
from notification_repository import NotificationRepository
from tasks import send_notification_task
import os

DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True 
)

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

def configure(binder: Binder):
    '''
    Контейнер для DI.
    '''
    binder.bind(Session, to=lambda: SessionLocal(), scope=singleton)
    binder.bind(NotificationRepository, scope=singleton)



api = Blueprint('api_v1', __name__, url_prefix='/api/v1')

@api.route('/notifications', methods=['POST'])
def create_notification(db : NotificationRepository):
    '''
    Создает уведомление и отправляет его в очередь сообщений.
    '''
    logger = logging.getLogger('werkzeug')
    logger.info("Creating new notification")

    payload = None
    try:
        json_data = request.get_json() or {}
        payload = NotificationCreate(**json_data)
    except ValidationError as e:
        logger.error("Invalid data. Cannot create new notification")
        return jsonify(e.errors()), 400

    notification = Notification(
        type=payload.type,
        recipient=payload.recipient,
        subject=payload.subject,
        message=payload.message,
        status=NotificationStatus.QUEUED,
        channel_data=payload.channel_data 
    )

    created = db.create(notification)
    logger.info(f"Created new notification with id {created.id}")

    logger.info(f"Sending notification {created.id} to queue")
    send_notification_task.delay(str(created.id))
    logger.info(f"Notification {created.id} was sent to queue")

    response_data = NotificationCreateResponse(
        id= created.id,
        status=created.status
    )
    
    return jsonify(response_data.model_dump()), 201

@api.route('/notifications/<uuid:id>', methods=['GET'])
def get_notification(id : str, db : NotificationRepository):
    '''
    Возвращает уведомление по id.
    '''
    logger = logging.getLogger('werkzeug')

    logger.info(f"Searching notification with id {id}")
    found = db.get_by_id(id)

    if not found:
        logger.error(f"Cannot found notification with id {id}")
        return jsonify({"error": "Not found"}), 404
    
    logger.info(f"Found notification with id {id}")

    response_data = NotificationReadResponse(
        id=found.id,
        status=found.status,
        error_text=found.error_text
    )
    
    return jsonify(response_data.model_dump()), 200

@api.route('/notifications', methods=['GET'])
def list_notifications(db : NotificationRepository):
    '''
    Возвращает лист уведомлений с фильтрацией и пагинацией.
    '''
    logger = logging.getLogger('werkzeug')

    try:
        params = NotificationFilter(
            offset = request.args.get("offset", default = 0),
            limit = request.args.get("limit", default = 10),
            status = request.args.get("status"),
        )
    except ValidationError as e:
        logger.error("Invalid request params")
        return jsonify(e.errors()), 400

    logger.info("Searching list of notifications for request")
    found = db.get_list(
        params.limit, 
        params.offset,
        params.status
    )
    logger.info("List of notifications found")

    result = [
        NotificationReadResponse(
            id=f.id,
            status=f.status,
            error_text=f.error_text
        ).model_dump()
        for f in found
    ]
    
    return jsonify(result), 200

app = Flask(__name__)
app.register_blueprint(api)
FlaskInjector(app=app, modules=[configure])

if __name__ == '__main__':
    run_migrations()
    app.run(host='0.0.0.0', port=5000, debug=False)