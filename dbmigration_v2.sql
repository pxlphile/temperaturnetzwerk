-- run first part

ALTER TABLE temperatur ADD COLUMN sensorId TEXT NOT NULL DEFAULT '';
CREATE INDEX sensorIdx ON temperatur(sensorId);
UPDATE temperatur SET sensorId = "28-0316049898ff" WHERE sensorId = "";

DROP INDEX sensorIdx;
DROP INDEX colDateIdx;

-- run createDb.py here

-- run second part
ALTER TABLE temperatur rename to temperatur_old;
INSERT INTO temperatur(id, tempdate, temperature, sensorId) select id,datum,temp,sensorId from temperatur_old;
DROP TABLE temperatur_old;
VACUUM temperatur;