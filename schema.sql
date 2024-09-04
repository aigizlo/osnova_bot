
CREATE TABLE users (
    user_id BIGINT,
    referer_id BIGINT,
    first_name VARCHAR(255),
    lastname VARCHAR(255),
    username VARCHAR(255),
    admin BOOL NOT NULL DEFAULT false,
    data TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    subscription_id INTEGER,
    FOREIGN KEY (subscription_id) REFERENCES subscriptions(subscription_id)
);

CREATE TABLE subscriptions (
    subscription_id INTEGER PRIMARY KEY,
    duration_months INTEGER,
    price DECIMAL(10, 2)
);

CREATE TABLE transactions (
    transaction_id INTEGER PRIMARY KEY,
    user_id BIGINT,
    subscription_id INTEGER,
    promo_id INTEGER,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    amount_paid DECIMAL(10, 2),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (subscription_id) REFERENCES subscriptions(subscription_id),
    FOREIGN KEY (promo_id) REFERENCES promo_codes(promo_id)
);

CREATE TABLE promo_codes (
    promo_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) NOT NULL UNIQUE,
    discount_percent INTEGER NOT NULL CHECK (discount_percent BETWEEN 0 AND 100),
    valid_until DATE NOT NULL
);

CREATE TABLE balance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    transaction_type ENUM('referral', 'add_balance', 'withdraw') NOT NULL,
    description VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);