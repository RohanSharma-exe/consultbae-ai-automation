from etl.matching import find_match


PEOPLE = [
    {
        "person_id": 1,
        "canonical_name": "Rohit Verma",
        "email": "rohit.verma13@mailtest.example.org",
        "phone": "9000000294",
        "city": "Delhi",
    },
    {
        "person_id": 2,
        "canonical_name": "Arjun Mehta",
        "email": "arjun.mehta@mailtest.example.org",
        "phone": "9000000131",
        "city": "Mumbai",
    },
]


def test_exact_email_match():
    result = find_match(
        {
            "name": "R. Verma",
            "email": "rohit.verma13@mailtest.example.org",
            "phone": "9000000294",
            "city": "Delhi",
        },
        PEOPLE,
    )

    assert result.matched_person_id == 1
    assert result.method == "exact_email"
    assert result.confidence == 1.0


def test_exact_phone_match():
    result = find_match(
        {
            "name": "Arjun Mehta",
            "email": "different@example.org",
            "phone": "9000000131",
            "city": "Mumbai",
        },
        PEOPLE,
    )

    assert result.matched_person_id == 2
    assert result.method == "exact_phone"


def test_name_city_match():
    people = [
        {
            "person_id": 3,
            "canonical_name": "Tanvi Gupta",
            "email": None,
            "phone": None,
            "city": "Pune",
        }
    ]

    result = find_match(
        {
            "name": "tanvi gupta",
            "email": None,
            "phone": None,
            "city": "PUNE",
        },
        people,
    )

    assert result.matched_person_id == 3
    assert result.method == "exact_name_city"


def test_same_name_different_city_is_not_automatically_matched():
    people = [
        {
            "person_id": 4,
            "canonical_name": "Deepak Nair",
            "email": "deepak.one@example.org",
            "phone": "9000000111",
            "city": "Delhi",
        }
    ]

    result = find_match(
        {
            "name": "Deepak Nair",
            "email": "deepak.two@example.org",
            "phone": "9000000222",
            "city": "Mumbai",
        },
        people,
    )

    assert result.matched_person_id is None
    assert result.method == "no_match"


def test_ambiguous_name_city_requires_review():
    people = [
        {
            "person_id": 5,
            "canonical_name": "Same Name",
            "email": "one@example.org",
            "phone": "9000000001",
            "city": "Pune",
        },
        {
            "person_id": 6,
            "canonical_name": "Same Name",
            "email": "two@example.org",
            "phone": "9000000002",
            "city": "Pune",
        },
    ]

    result = find_match(
        {
            "name": "Same Name",
            "email": None,
            "phone": None,
            "city": "Pune",
        },
        people,
    )

    assert result.matched_person_id is None
    assert result.needs_review is True
    assert result.method == "ambiguous_name_city"