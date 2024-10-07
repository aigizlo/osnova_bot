CREATE TABLE users (
    user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    telegram_id INT NOT NULL UNIQUE
    referer_id INT DEFAULT NULL,
    free_tariff INT NOT NULL DEFAULT '0'
    admin INT NOT NULL DEFAULT '0'
);

CREATE TABLE user_balance_ops (
    user_id INT NOT NULL,
    opdate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    optype ENUM('addmoney', 'payment', 'correction', 'bonus') NOT NULL,
    key_id INT,         # ссылка на ключ для payment
    trx_id VARCHAR(32), # ID транзакции в платёжной системе для payment
    amount INT NOT NULL # рубли
);

CREATE TABLE new_users (
    user_id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    telegram_id BIGINT,
    referer_id INT,
    free_tariff INT NOT NULL DEFAULT 0,
    admin INT NOT NULL DEFAULT 0,
    lastname VARCHAR(255),
    nickname VARCHAR(255),
    premium VARCHAR(255),
    language VARCHAR(255),
    date_accession DATE,
    message INT NOT NULL DEFAULT 0,
    PRIMARY KEY (user_id)
);

CREATE TABLE servers (
    server_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    country VARCHAR(64) NOT NULL
);


CREATE TABLE outline_keys (
    key_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    outline_key_id INT NOT NULL,
    server_id INT NOT NULL,
    key_value VARCHAR(255) NOT NULL,
    used TINYINT(1) NOT NULL
);
