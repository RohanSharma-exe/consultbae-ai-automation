PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS persons (
    person_id INTEGER PRIMARY KEY AUTOINCREMENT,
    canonical_name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    city TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_persons_email
ON persons(email)
WHERE email IS NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS idx_persons_phone
ON persons(phone)
WHERE phone IS NOT NULL;


CREATE TABLE IF NOT EXISTS source_records (
    source_record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER,
    source_name TEXT NOT NULL,
    source_row_id TEXT,
    raw_name TEXT,
    raw_email TEXT,
    raw_phone TEXT,
    raw_city TEXT,
    raw_payload TEXT NOT NULL,
    match_method TEXT,
    match_confidence REAL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (person_id)
        REFERENCES persons(person_id)
);


CREATE TABLE IF NOT EXISTS person_skills (
    person_skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER NOT NULL,
    skill TEXT NOT NULL,
    source_name TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (person_id)
        REFERENCES persons(person_id)
);


CREATE TABLE IF NOT EXISTS skill_categories (
    person_id INTEGER PRIMARY KEY,
    category TEXT NOT NULL,
    source TEXT NOT NULL,
    confidence REAL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (person_id)
        REFERENCES persons(person_id)
);


CREATE TABLE IF NOT EXISTS audio_submissions (
    submission_id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER NOT NULL,
    original_filename TEXT NOT NULL,
    stored_filename TEXT NOT NULL,
    file_path TEXT NOT NULL,

    duration_seconds REAL,
    sample_rate_khz REAL,
    bitrate_kbps REAL,
    loudness_db REAL,
    quality_score REAL,

    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (person_id)
        REFERENCES persons(person_id)
);


CREATE INDEX IF NOT EXISTS idx_source_records_person_id
ON source_records(person_id);

CREATE INDEX IF NOT EXISTS idx_person_skills_person_id
ON person_skills(person_id);

CREATE INDEX IF NOT EXISTS idx_audio_submissions_person_id
ON audio_submissions(person_id);