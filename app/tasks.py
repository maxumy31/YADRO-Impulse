from celery import Celery
from model import *
from uuid import UUID
from notification_repository import NotificationRepository
from sqlalchemy.orm import sessionmaker, Session
from celery.utils.log import get_task_logger
from sqlalchemy import create_engine
import os

DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL")

celery_app = Celery('notifications', broker=REDIS_URL)
logger = get_task_logger(__name__)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@celery_app.task(bind=True)
def send_notification_task(self, notification_id: str) -> None:
    '''
    Отправляет уведомление по соответствующему каналу
    '''
    with SessionLocal() as session:
        db = NotificationRepository(session)
        notification = db.get_by_id(notification_id)
        
        if not notification:
            logger.info(f"Notification not found by id {notification_id}")
            return
        
        if notification.status == NotificationStatus.SENT:
            logger.info(f"Notification {notification_id} already sent")
            return
        
        print(f"Starting delivery for {notification_id}")

        result = False
        error = None
        try:
            result = send_message_mock(notification)
        except Exception as e:
            error = str(e)
            result = False

        if result:
            db.update_status(notification.id, NotificationStatus.SENT)
            logger.info(f"Notification {notification_id} was sent")
        else:
            logger.error(f"Notification {notification_id} was failed with error {error}")
            db.update_status(notification.id, NotificationStatus.FAILED, error or "Unknown error") 


def send_message_mock(notification : Notification) -> bool:
    '''
    Симулирует отправку сообщения и логирует завершение выполнения.
    '''
    match notification.type:
        case NotificationType.TELEGRAM:
            logger.info("Sending telegram message")
        case NotificationType.SMS:
            logger.info("Sending sms message")
        case NotificationType.EMAIL:
            logger.info("Sending email message")

    return True