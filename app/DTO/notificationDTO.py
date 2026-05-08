import re
from typing import Optional, Any, Dict
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator, ConfigDict, Field, EmailStr
from model import NotificationType, NotificationStatus
from validators import *

class NotificationCreate(BaseModel):
    '''
    DTO для создания уведомлений.
    '''
    model_config = ConfigDict(from_attributes=True)
    type: NotificationType
    recipient: str = Field(..., min_length=1, max_length=255)
    subject: Optional[str] = Field(None, max_length=500)
    message: str = Field(..., min_length=1)
    channel_data: Optional[Dict[str, Any]] = None

    @model_validator(mode='after')
    def validate_recipient_format(self) -> 'NotificationCreate':
        v_type = self.type
        v_recipient = self.recipient

        if v_type == NotificationType.EMAIL:
            if not is_valid_email(v_recipient):
                raise ValueError("Invalid email format")
        elif v_type == NotificationType.SMS:
            if not is_valid_phone(v_recipient):
                raise ValueError("SMS recipient must be a phone number in E.164 format (+1234567890)")
        elif v_type == NotificationType.TELEGRAM:
            if not is_valid_telegram(v_recipient):
                raise ValueError("Telegram recipient must be a numeric ID or @username")

        return self

class NotificationCreateResponse(BaseModel):
    '''
    DTO для ответа на создание уведомлений.
    '''
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    status: NotificationStatus

class NotificationReadResponse(BaseModel):
    '''
    DTO для ответа на чтение уведомлений.
    '''
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    status: NotificationStatus
    error: Optional[str] = None

class NotificationFilter(BaseModel):
    '''
    DTO для фильтрации уведомлений.
    '''
    status: Optional[NotificationStatus] = None
    limit: int = Field(10, ge=1, le=100)
    offset: int = Field(0, ge=0)
