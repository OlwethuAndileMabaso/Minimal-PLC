-- Minimal-PLC SQLite Schema
-- Run once to initialise the database, safe to re-run (IF NOT EXISTS).

CREATE TABLE IF NOT EXISTS history (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    point_name TEXT    NOT NULL,
    value      TEXT    NOT NULL,
    quality    TEXT    NOT NULL DEFAULT 'good',
    ts         REAL    NOT NULL   -- Unix timestamp (float seconds)
);

CREATE INDEX IF NOT EXISTS idx_history_point_ts
    ON history (point_name, ts DESC);

-- -----------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS alarms (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    point_name TEXT    NOT NULL,
    message    TEXT    NOT NULL,
    severity   TEXT    NOT NULL DEFAULT 'warning',  -- info | warning | critical
    acknowledged INTEGER NOT NULL DEFAULT 0,
    ts         REAL    NOT NULL   -- Unix timestamp when alarm triggered
);

CREATE INDEX IF NOT EXISTS idx_alarms_ts
    ON alarms (ts DESC);

-- -----------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS config (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
