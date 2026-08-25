from etl.normalize import (
    normalize_city,
    normalize_email,
    normalize_name,
    normalize_phone,
    normalize_skills,
    normalize_status,
    normalize_verified,
    parse_ctc_lpa,
    parse_rate,
)


def test_normalize_email():
    assert normalize_email("  JOHN.DOE@EXAMPLE.COM ") == "john.doe@example.com"


def test_normalize_phone():
    assert normalize_phone("+91-9000000131") == "9000000131"
    assert normalize_phone("919000000131") == "9000000131"
    assert normalize_phone("9000000131") == "9000000131"


def test_normalize_name():
    assert normalize_name("  rohit   verma ") == "Rohit Verma"


def test_normalize_city():
    assert normalize_city("  PUNE ") == "Pune"


def test_normalize_status():
    assert normalize_status(" ACTIVE ") == "active"


def test_normalize_verified():
    assert normalize_verified("Y") is True
    assert normalize_verified("yes") is True
    assert normalize_verified("N") is False
    assert normalize_verified("No") is False


def test_normalize_skills():
    assert normalize_skills("React, JavaScript, MySQL") == [
        "react",
        "javascript",
        "mysql",
    ]


def test_parse_ctc_lpa():
    assert parse_ctc_lpa("4.2") == 4.2
    assert parse_ctc_lpa("417964") == 4.17964


def test_parse_rate():
    assert parse_rate("1415/hr") == (1415.0, "hour")
    assert parse_rate("15k/month") == (15000.0, "month")