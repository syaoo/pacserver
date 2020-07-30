drop table if exists rules;
create table rules (
  id integer primary key autoincrement,
  rule TEXT not null
);

DROP TABLE IF EXISTS users;
CREATE TABLE users(
  id integer primary key autoincrement,
  name VARCHAR(25) NOT NULL,
  email VARCHAR(25) NOT NULL UNIQUE,
  passwd VARCHAR(25) NOT NULL
);