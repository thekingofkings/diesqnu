BEGIN;
CREATE TABLE `quote_record` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `company` varchar(200) NOT NULL,
    `phone` integer NOT NULL,
    `price` double precision NOT NULL,
    `duration` integer NOT NULL
)
;

COMMIT;
