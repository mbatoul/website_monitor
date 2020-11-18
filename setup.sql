CREATE TABLE IF NOT EXISTS data_points
(
  id SERIAL PRIMARY KEY NOT NULL,
  website VARCHAR NOT NULL,
  response_code INT NOT NULL,
  response_time REAL NOT NULL,
  time TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS alerts
(
  id SERIAL PRIMARY KEY NOT NULL,
  website VARCHAR NOT NULL,
  is_running BOOLEAN NOT NULL DEFAULT TRUE,
  start_time TIMESTAMP NOT NULL DEFAULT NOW(),
  start_availability REAL NOT NULL,
  end_time TIMESTAMP,
  end_availability REAL
);