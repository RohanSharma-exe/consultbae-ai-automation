import sqlite3
from pathlib import Path



PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "consultbae.db"
SCHEMA_PATH = PROJECT_ROOT / "etl" / "schema.sql"


def initialize_database() -> None:
    schema = SCHEMA_PATH.read_text(encoding="utf-8")

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.executescript(schema)

    print(f"Database initialized: {DATABASE_PATH}")


if __name__ == "__main__":
    initialize_database()