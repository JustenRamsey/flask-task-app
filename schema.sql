DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS users;


-- add foreign key to connect users table to the tasks table 

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL 

);

CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    time_minutes INTEGER NOT NULL,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id)
);


-- Should I change the user table to be the primary table and then make the "id" in the task table a foreign key to connect both tables? 
-- FOREIGN KEY ("id") REFERENCES "tasks" id 
