from dataclasses import dataclass
from typing import Any


@dataclass
class MatchResult:
    matched_person_id: int | None
    method: str
    confidence: float
    needs_review: bool = False


def _normalized_name(name: Any) -> str | None:
    if name is None:
        return None

    value = str(name).strip().lower()

    if not value:
        return None

    return " ".join(value.split())


def find_match(
    record: dict[str, Any],
    people: list[dict[str, Any]],
) -> MatchResult:
    """
    Find the best existing person for a normalized source record.

    Matching priority:

    1. Exact email
    2. Exact phone
    3. Exact name + city

    Name alone is never considered sufficient.
    """

    email = record.get("email")
    phone = record.get("phone")
    name = _normalized_name(record.get("name"))
    city = _normalized_name(record.get("city"))

    # ---------------------------------------------------------
    # Tier 1: exact email
    # ---------------------------------------------------------

    if email:
        email_matches = [
            person
            for person in people
            if person.get("email") == email
        ]

        if len(email_matches) == 1:
            return MatchResult(
                matched_person_id=email_matches[0]["person_id"],
                method="exact_email",
                confidence=1.0,
            )

        if len(email_matches) > 1:
            return MatchResult(
                matched_person_id=None,
                method="conflicting_email",
                confidence=0.0,
                needs_review=True,
            )

    # ---------------------------------------------------------
    # Tier 2: exact phone
    # ---------------------------------------------------------

    if phone:
        phone_matches = [
            person
            for person in people
            if person.get("phone") == phone
        ]

        if len(phone_matches) == 1:
            return MatchResult(
                matched_person_id=phone_matches[0]["person_id"],
                method="exact_phone",
                confidence=0.95,
            )

        if len(phone_matches) > 1:
            return MatchResult(
                matched_person_id=None,
                method="conflicting_phone",
                confidence=0.0,
                needs_review=True,
            )

    # ---------------------------------------------------------
    # Tier 3: exact name + city
    # ---------------------------------------------------------

    if name and city:
        name_city_matches = [
            person
            for person in people
            if (
                _normalized_name(person.get("canonical_name")) == name
                and _normalized_name(person.get("city")) == city
            )
        ]

        if len(name_city_matches) == 1:
            return MatchResult(
                matched_person_id=name_city_matches[0]["person_id"],
                method="exact_name_city",
                confidence=0.75,
            )

        if len(name_city_matches) > 1:
            return MatchResult(
                matched_person_id=None,
                method="ambiguous_name_city",
                confidence=0.0,
                needs_review=True,
            )

    # ---------------------------------------------------------
    # No sufficiently strong match
    # ---------------------------------------------------------

    return MatchResult(
        matched_person_id=None,
        method="no_match",
        confidence=0.0,
    )