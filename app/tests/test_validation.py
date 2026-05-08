import pytest
from validators import is_valid_email, is_valid_phone, is_valid_telegram


@pytest.mark.parametrize("email, expected", [
    ("user@example.com", True),
    ("invalid-email.com", False),
    ("name@domain..com", True),
])
def test_is_valid_email(email, expected):
    assert is_valid_email(email) == expected

@pytest.mark.parametrize("phone, expected", [
    ("+12345678901", True),
    ("12345678901", False),
    ("+12345", False),
])
def test_is_valid_phone(phone, expected):
    assert is_valid_phone(phone) == expected

@pytest.mark.parametrize("tg_contact, expected", [
    ("@username", True),
    ("123456789", True),
    ("username_without_at", False),
])
def test_is_valid_telegram(tg_contact, expected):
    assert is_valid_telegram(tg_contact) == expected