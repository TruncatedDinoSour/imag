-- Migration for version 1.0.0: Score support

ALTER TABLE image ADD COLUMN score INTEGER;
UPDATE image SET score=0;
