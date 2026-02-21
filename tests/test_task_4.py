import pytest

import tasks.task_4 as task4
from tasks.task_4 import (
    parse_input,
    validate_phone,
    add_contact,
    update_contact,
    get_users_phone,
    ERR_NAME_AND_PHONE,
)


@pytest.fixture(autouse=True)
def clear_users():
    task4.USERS.clear()
    yield
    task4.USERS.clear()


# --- parse_input ---


def test_parse_input_command_and_args():
    cmd, args = parse_input("add john 1234567890")
    assert cmd == "add"
    assert args == ["john", "1234567890"]


def test_parse_input_command_only():
    cmd, args = parse_input("hello")
    assert cmd == "hello"
    assert args == []


def test_parse_input_empty_string():
    cmd, args = parse_input("")
    assert cmd == ""
    assert args == []


def test_parse_input_lowercases_command():
    cmd, _ = parse_input("ADD john 1234567890")
    assert cmd == "add"


def test_parse_input_extra_whitespace():
    cmd, args = parse_input("  phone   john  ")
    assert cmd == "phone"
    assert args == ["john"]


# --- validate_phone ---


def test_validate_phone_valid_10_digits():
    validate_phone("1234567890")  # should not raise


def test_validate_phone_valid_with_formatting():
    validate_phone("+1 (234) 567-890.1")  # should not raise


def test_validate_phone_too_short_raises():
    with pytest.raises(ValueError, match="not matching valid format"):
        validate_phone("12345")


def test_validate_phone_too_long_raises():
    with pytest.raises(ValueError, match="not matching valid format"):
        validate_phone("1234567890123456")


def test_validate_phone_letters_raises():
    with pytest.raises(ValueError, match="not matching valid format"):
        validate_phone("abcdefghij")


# --- add_contact ---


def test_add_contact_success():
    result = add_contact(["john", "1234567890"])
    assert "Contact added." in result
    assert task4.USERS["John"] == "1234567890"


def test_add_contact_capitalises_username():
    add_contact(["alice", "1234567890"])
    assert "Alice" in task4.USERS


def test_add_contact_missing_args_returns_error():
    result = add_contact(["john"])
    assert ERR_NAME_AND_PHONE in result


def test_add_contact_no_args_returns_error():
    result = add_contact([])
    assert ERR_NAME_AND_PHONE in result


def test_add_contact_invalid_phone_returns_error():
    result = add_contact(["john", "123"])
    assert "not matching valid format" in result


def test_add_contact_duplicate_prints_error(capsys):
    add_contact(["john", "1234567890"])
    result = add_contact(["john", "1234567890"])
    assert result is None
    assert "already exists" in capsys.readouterr().out


# --- update_contact ---


def test_update_contact_success():
    task4.USERS["John"] = "1234567890"
    result = update_contact(["john", "0987654321"])
    assert "Contact updated." in result
    assert task4.USERS["John"] == "0987654321"


def test_update_contact_user_not_found_returns_error():
    result = update_contact(["unknown", "1234567890"])
    assert "doesn't exist" in result


def test_update_contact_missing_args_returns_error():
    result = update_contact(["john"])
    assert ERR_NAME_AND_PHONE in result


def test_update_contact_invalid_phone_returns_error():
    task4.USERS["John"] = "1234567890"
    result = update_contact(["john", "bad"])
    assert "not matching valid format" in result


# --- get_users_phone ---


def test_get_users_phone_success():
    task4.USERS["John"] = "1234567890"
    result = get_users_phone(["john"])
    assert "1234567890" in result


def test_get_users_phone_no_args_returns_error():
    result = get_users_phone([])
    assert "Enter user name." in result


def test_get_users_phone_user_not_found_returns_error():
    result = get_users_phone(["ghost"])
    assert "doesn't exist" in result


def test_get_users_phone_case_insensitive():
    task4.USERS["Alice"] = "1234567890"
    result = get_users_phone(["ALICE"])
    assert "1234567890" in result
