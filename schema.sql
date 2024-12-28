-- Table for storing user information
CREATE TABLE users (
    -- Unique user ID
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    -- Username for login
    username TEXT NOT NULL UNIQUE,
    -- Hashed password for security
    password_hash TEXT NOT NULL
);

-- Table for storing health metrics: blood pressure records
CREATE TABLE blood_pressure (
    -- Unique record ID
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    -- ID of the user who owns this record
    user_id INTEGER NOT NULL,
    -- Systolic blood pressure
    systolic INTEGER NOT NULL,
    -- Diastolic blood pressure
    diastolic INTEGER NOT NULL,
    -- Pulse
    pulse INTEGER  NOT NULL,
    -- Date and time of the measurement
    date_time TEXT NOT NULL,
    -- Foreign key linking to users table
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Table for storing health metrics: weight records
CREATE TABLE weight (
    -- Unique record ID
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    -- ID of the user who owns this record
    user_id INTEGER NOT NULL,
    -- Weight value in kilograms
    weight_value REAL NOT NULL,
    -- Date and time of the measurement
    date_time TEXT NOT NULL,
    -- Foreign key linking to users table
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Table for storing health metrics: medication records
CREATE TABLE medications (
    -- Unique record ID
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    -- ID of the user who owns this record
    user_id INTEGER NOT NULL,
    -- Name of the medication
    medication_name TEXT NOT NULL,
    -- Dosage information (optional)
    dosage TEXT,
    -- Date and time of the record
    date_time TEXT NOT NULL,
    -- Whether the medication was taken (0 = no, 1 = yes)
    taken BOOLEAN NOT NULL CHECK (taken IN (0, 1)),
    -- Foreign key linking to users table
    FOREIGN KEY (user_id) REFERENCES users (id)
);
