DROP TABLE IF EXISTS samples;

CREATE TABLE samples
(
  id INTEGER PRIMARY KEY,
  sourceId TEXT NOT NULL,
  timestamp INTEGER NOT NULL,
  latitude REAL NOT NULL,
  longitude REAL NOT NULL,
  temperature REAL NOT NULL,
  salinity REAL NOT NULL
);
