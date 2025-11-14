CREATE TABLE IF NOT EXISTS device_logs (
  deviceId TEXT NOT NULL,
  timestamp INTEGER NOT NULL,
  data TEXT NOT NULL,
  PRIMARY KEY (deviceId, timestamp)
);