import enum
from datetime import datetime, timezone
from uuid import UUID, uuid4
from typing import Any
from sqlalchemy import String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

class Base(DeclarativeBase):
    pass


class NotificationType(str, enum.Enum):
    '''
    Типы уведомлений.
    '''
    EMAIL = "email"
    TELEGRAM = "telegram"
    SMS = "sms"


class NotificationStatus(str, enum.Enum):
    '''
    Статусы уведомлений.
    '''
    QUEUED = "queued"
    SENT = "sent"
    FAILED = "failed"


class Notification(Base):
    '''
    Модель уведомления.
    '''
    __tablename__ = "notifications"

    id: Mapped[UUID] = mapped_column(
        primary_key=True, 
        default=uuid4
    )
    
    type: Mapped[NotificationType] = mapped_column(
        nullable=False
    )
    
    recipient: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    subject: Mapped[str | None] = mapped_column(String(500))
    message: Mapped[str] = mapped_column(Text, nullable=False)
    
    status: Mapped[NotificationStatus] = mapped_column(
        default=NotificationStatus.QUEUED,
        index=True
    )
    
    error_text: Mapped[str | None] = mapped_column(Text)

    channel_data: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        insert_default=func.now()
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        insert_default=func.now(),
        onupdate=func.now()
    )
