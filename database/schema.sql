PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS liveness_sessions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_ref TEXT NOT NULL UNIQUE,
  device_ref TEXT,
  status TEXT NOT NULL DEFAULT 'OPEN' CHECK(status IN ('OPEN','DECIDED')),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS signal_observations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id INTEGER NOT NULL,
  texture_score REAL NOT NULL CHECK(texture_score BETWEEN 0 AND 1),
  motion_score REAL NOT NULL CHECK(motion_score BETWEEN 0 AND 1),
  depth_score REAL NOT NULL CHECK(depth_score BETWEEN 0 AND 1),
  captured_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(session_id) REFERENCES liveness_sessions(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS challenge_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id INTEGER NOT NULL,
  challenge_type TEXT NOT NULL,
  passed INTEGER NOT NULL CHECK(passed IN (0,1)),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(session_id) REFERENCES liveness_sessions(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS liveness_decisions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id INTEGER NOT NULL UNIQUE,
  label TEXT NOT NULL CHECK(label IN ('GENUINE','SPOOF')),
  score REAL NOT NULL CHECK(score BETWEEN 0 AND 1),
  threshold REAL NOT NULL CHECK(threshold BETWEEN 0 AND 1),
  model_version TEXT NOT NULL DEFAULT 'fusion-baseline-v1',
  explanation TEXT NOT NULL DEFAULT '',
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(session_id) REFERENCES liveness_sessions(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_signal_session ON signal_observations(session_id);
CREATE INDEX IF NOT EXISTS idx_challenge_session ON challenge_events(session_id);
