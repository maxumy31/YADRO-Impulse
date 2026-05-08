from uuid import UUID
from typing import Sequence, Optional
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from model import *
from injector import inject

class NotificationRepository:
    '''
    Взаимодействует с таблицей notifications.
    '''
    @inject
    def __init__(self, session: Session):
        self.session = session

    def create(self, notification: Notification) -> Notification:
        '''
        Создает новое уведомление.
        '''
        self.session.add(notification)
        self.session.commit()
        self.session.refresh(notification)
        return notification

    def get_by_id(self, notification_id: UUID) -> Optional[Notification]:
        '''
        Возвращает уведомление по его id.
        '''
        query = select(Notification).where(Notification.id == notification_id)
        result = self.session.execute(query)
        return result.scalar_one_or_none()

    def get_list(
            self, 
            limit: int = 10, 
            offset: int = 0, 
            status: Optional[str] = None
        ) -> Sequence[Notification]:
        '''
        Возвращает список уведомлений с фильтрацией по статусу и пагинацией.
        '''
        query = (
            select(Notification)
            .order_by(Notification.created_at.desc())
        )

        if status is not None:
            query = query.where(Notification.status == status)

        query = query.limit(limit).offset(offset)

        result = self.session.execute(query)
        return result.scalars().all()

    def get_next_queued(self) -> Optional[Notification]:
        '''
        Возвращает уведомление, которое не было отправлено.
        '''
        query = (
            select(Notification)
            .where(Notification.status == NotificationStatus.QUEUED)
            .order_by(Notification.created_at.asc())
            .limit(1)
        )
        return self.session.execute(query).scalar_one_or_none()
    
    def update_status(
            self, 
            notification_id: UUID, 
            status: NotificationStatus, 
            error_text: Optional[str] = None
        ) -> None:
        '''
        Обновляет статус уведомления по его id и ставит значенин текста ошибки.
        '''
        stmt = (
            update(Notification)
            .where(Notification.id == notification_id)
            .values(status=status, error_text=error_text)
        )
        self.session.execute(stmt)
        self.session.commit()