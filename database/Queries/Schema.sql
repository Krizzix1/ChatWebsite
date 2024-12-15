-- SQLite
CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userName TEXT UNIQUE,
    password TEXT
);

CREATE TABLE chatRoom(
    id INTEGER,
    user TEXT,
    PRIMARY KEY (id,user)
    FOREIGN KEY (user) REFERENCES users(userName)

);

CREATE TABLE messages(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender TEXT,
    roomReceiver INTEGER,
    FOREIGN KEY(roomReceiver) REFERENCES chatRoom(id)
    FOREIGN KEY(sender) REFERENCES users(userName)
);

CREATE TABLE friends(
    userNameA TEXT,
    userNameB TEXT,
    PRIMARY KEY(userNameA, userNameB),
    FOREIGN KEY(userNameA) REFERENCES users(userName),
    FOREIGN KEY(userNameB) REFERENCES users(userName)
);