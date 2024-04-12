-- Migration for version 3.1.0: Added "delete" role

BEGIN TRANSACTION;
ALTER TABLE access_key RENAME TO old_access_key;
CREATE TABLE access_key (
    "key" VARCHAR(128) NOT NULL,
    access_level VARCHAR(6),
    PRIMARY KEY ("key"),
    UNIQUE ("key")
);
INSERT INTO access_key SELECT * FROM old_access_key;
DROP TABLE old_access_key;
COMMIT;
