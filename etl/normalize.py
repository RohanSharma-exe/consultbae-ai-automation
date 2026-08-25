import re
from typing import Any


def clean_text(value: Any) -> str | None:
    """Trim whitespace and convert empty values to None."""
    if value is None:
        return None

    text = str(value).strip()

    if not text:
        return None

    return text


def normalize_name(value: Any) -> str | None:
    """Normalize a person's name while preserving readable casing."""
    text = clean_text(value)

    if text is None:
        return None

    return " ".join(text.split()).title()


def normalize_email(value: Any) -> str | None:
    """Normalize an email address."""
    text = clean_text(value)

    if text is None:
        return None

    return text.lower()


def normalize_phone(value: Any) -> str | None:
    """
    Normalize an Indian phone number to its final 10 digits.

    Examples:
        +91-9000000131 -> 9000000131
        919000000131   -> 9000000131
        9000000131     -> 9000000131
    """
    text = clean_text(value)

    if text is None:
        return None

    digits = re.sub(r"\D", "", text)

    if digits.startswith("91") and len(digits) == 12:
        digits = digits[2:]

    if len(digits) == 10:
        return digits

    return digits or None


def normalize_city(value: Any) -> str | None:
    """Normalize city names."""
    text = clean_text(value)

    if text is None:
        return None

    return " ".join(text.split()).title()


def normalize_status(value: Any) -> str | None:
    """Normalize worker status values."""
    text = clean_text(value)

    if text is None:
        return None

    return text.lower()


def normalize_verified(value: Any) -> bool | None:
    """
    Normalize CBNexus verification values.

    Accepted true values:
        Y, yes, true, 1

    Accepted false values:
        N, no, false, 0
    """
    text = clean_text(value)

    if text is None:
        return None

    normalized = text.lower()

    if normalized in {"y", "yes", "true", "1"}:
        return True

    if normalized in {"n", "no", "false", "0"}:
        return False

    return None


def normalize_skills(value: Any) -> list[str]:
    """Convert a comma-separated skill field into normalized skill names."""
    text = clean_text(value)

    if text is None:
        return []

    skills = []

    for skill in text.split(","):
        normalized = skill.strip().lower()

        if normalized:
            skills.append(normalized)

    return skills


def parse_ctc_lpa(value: Any) -> float | None:
    """
    Normalize current CTC into LPA.

    The source data contains both values that already look like LPA
    and larger numeric values that appear to represent annual salary
    in rupees.

    Values greater than 100,000 are therefore interpreted as INR
    and converted to LPA.
    """
    text = clean_text(value)

    if text is None:
        return None

    try:
        numeric_value = float(text.replace(",", ""))
    except ValueError:
        return None

    if numeric_value > 100_000:
        return numeric_value / 100_000

    return numeric_value


def parse_rate(value: Any) -> tuple[float | None, str | None]:
    """
    Parse gig-worker rates.

    Examples:
        1415/hr    -> (1415, "hour")
        15k/month  -> (15000, "month")
        72k/month  -> (72000, "month")
    """
    text = clean_text(value)

    if text is None:
        return None, None

    normalized = text.lower().replace(",", "").replace(" ", "")

    match = re.fullmatch(
        r"(\d+(?:\.\d+)?)(k)?/(hr|hour|month|mo)",
        normalized,
    )

    if not match:
        return None, None

    amount = float(match.group(1))

    if match.group(2) == "k":
        amount *= 1_000

    unit = match.group(3)

    if unit in {"hr", "hour"}:
        unit = "hour"
    else:
        unit = "month"

    return amount, unit