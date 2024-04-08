-- migration for version 1.0.0

ALTER TABLE image ADD COLUMN score INTEGER;
UPDATE image SET score=0;
