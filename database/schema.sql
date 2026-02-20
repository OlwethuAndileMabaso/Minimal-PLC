-- database/schema.sql
-- Minimal-PLC SQLite schema
-- All tables use CREATE TABLE IF NOT EXISTS so this script is safe to re-run.

PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

-- ── Projects ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS projects (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL,
    description TEXT,
    hmi_config  TEXT,           -- JSON blob of HMI layout
    plc_program TEXT,           -- uploaded ST/IL source code
    created_at  TEXT    NOT NULL DEFAULT (datetime('now')),
    updated_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);

-- ── BACnet devices ────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS bacnet_devices (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    device_instance INTEGER NOT NULL UNIQUE,
    name            TEXT,
    ip_address      TEXT,
    port            INTEGER DEFAULT 47808,
    vendor          TEXT,
    last_seen       TEXT
);

-- ── BACnet points ─────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS bacnet_points (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id       INTEGER REFERENCES bacnet_devices(id) ON DELETE CASCADE,
    object_type     TEXT    NOT NULL,
    object_instance INTEGER NOT NULL,
    name            TEXT    NOT NULL,
    description     TEXT,
    unit            TEXT,
    min_value       REAL,
    max_value       REAL,
    alarm_low       REAL,
    alarm_high      REAL,
    last_value      REAL,
    last_updated    TEXT
);

-- ── Point history ─────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS point_history (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    point_id   INTEGER NOT NULL REFERENCES bacnet_points(id) ON DELETE CASCADE,
    value      REAL,
    quality    TEXT    DEFAULT 'good',
    timestamp  TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_point_history_point_ts
    ON point_history (point_id, timestamp);

-- ── Alarms ────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS alarms (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    point_id         INTEGER REFERENCES bacnet_points(id) ON DELETE SET NULL,
    alarm_type       TEXT,               -- HIGH, LOW, COMM, etc.
    message          TEXT,
    severity         TEXT DEFAULT 'low', -- critical, high, medium, low
    triggered_at     TEXT NOT NULL DEFAULT (datetime('now')),
    acknowledged_at  TEXT,
    acknowledged_by  TEXT
);

-- ── Users ─────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT    NOT NULL UNIQUE,
    password_hash TEXT    NOT NULL,
    role          TEXT    NOT NULL DEFAULT 'viewer', -- admin, engineer, operator, viewer
    email         TEXT,
    created_at    TEXT    NOT NULL DEFAULT (datetime('now')),
    last_login    TEXT,
    active        INTEGER NOT NULL DEFAULT 1
);

-- ── Network / platform configuration (key-value store) ───────────────────
CREATE TABLE IF NOT EXISTS network_config (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    key        TEXT    NOT NULL UNIQUE,
    value      TEXT,
    updated_at TEXT    NOT NULL DEFAULT (datetime('now'))
);

-- ── Audit log ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS audit_log (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER REFERENCES users(id) ON DELETE SET NULL,
    action     TEXT,
    details    TEXT,
    ip_address TEXT,
    timestamp  TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ── Default admin user ────────────────────────────────────────────────────
-- Password hash is bcrypt of "admin".  Change immediately after first login.
INSERT OR IGNORE INTO users (username, password_hash, role, email, active)
VALUES (
    'admin',
    '$2b$12$KIXiPSNHT3tHqAbK/yVfCeRFkGoTOD0bT89MEdZIl5LbRHGHbkVpu',
    'admin',
    'admin@localhost',
    1
);
