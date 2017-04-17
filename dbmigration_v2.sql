ALTER TABLE temperatur ADD COLUMN sensorId TEXT NOT NULL DEFAULT '';
CREATE INDEX sensorIdx ON temperatur(sensorId);
UPDATE temperatur SET sensorId = "28-0316049898ff" WHERE sensorId = "";
VACUUM temperatur;