DROP TABLE if EXISTS animals;
DROP TABLE if EXISTS accounts;
DROP TABLE if EXISTS messages;

CREATE TABLE animals(
    id integer PRIMARY KEY AUTOINCREMENT,
    entry text,
    family text,
    lifeSpan text,
    typeOf text
);
CREATE TABLE accounts(
    id integer PRIMARY KEY AUTOINCREMENT,
    user text NOT NULL,
    password text NOT NULL,
    avatar text
);
