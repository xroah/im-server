source db.sql;

CREATE TABLE IF NOT EXISTS account (
    userid INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(20) NOT NULL UNIQUE,
    password CHAR(32) NOT NULL,
    email VARCHAR(40),
    mobile INT(11),
    social_account VARCHAR(40) COMMENT "社交账户如微信等",
    social_type TINYINT,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modification_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);