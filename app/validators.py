import re

def is_valid_email(value: str) -> bool:
    '''
    Проверяет email на валидность.
    '''
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(email_regex, value))

def is_valid_phone(value: str) -> bool:
    '''
    Проверяет телефон на валидность.
    '''
    phone_regex = r'^\+\d{10,15}$'
    return bool(re.match(phone_regex, value))

def is_valid_telegram(value: str) -> bool:
    '''
    Проверяет телеграм на валидность.
    '''
    tg_regex = r'^[0-9]+$|^@\w+$'
    return bool(re.match(tg_regex, value))