-- Create review table
CREATE TABLE IF NOT EXISTS review (
    review_id VARCHAR(22) PRIMARY KEY,
    user_id VARCHAR(22) NOT NULL,
    business_id VARCHAR(22) NOT NULL,
    stars INTEGER NOT NULL CHECK (stars >= 1 AND stars <= 5),
    text TEXT NOT NULL,
    useful INTEGER DEFAULT 0,
    funny INTEGER DEFAULT 0,
    cool INTEGER DEFAULT 0,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_account(user_id),
    FOREIGN KEY (business_id) REFERENCES business(business_id)
);

-- Create tip table
CREATE TABLE IF NOT EXISTS tip (
    tip_id VARCHAR(22) PRIMARY KEY,
    user_id VARCHAR(22) NOT NULL,
    business_id VARCHAR(22) NOT NULL,
    text TEXT NOT NULL,
    compliment_count INTEGER DEFAULT 0,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_account(user_id),
    FOREIGN KEY (business_id) REFERENCES business(business_id)
);

-- Create review reactions table
CREATE TABLE IF NOT EXISTS review_reaction (
    user_id VARCHAR(22) NOT NULL,
    review_id VARCHAR(22) NOT NULL,
    reaction_type VARCHAR(10) NOT NULL CHECK (reaction_type IN ('useful', 'funny', 'cool')),
    PRIMARY KEY (user_id, review_id, reaction_type),
    FOREIGN KEY (user_id) REFERENCES user_account(user_id),
    FOREIGN KEY (review_id) REFERENCES review(review_id)
);

-- Create tip praises table
CREATE TABLE IF NOT EXISTS tip_praise (
    user_id VARCHAR(22) NOT NULL,
    tip_id VARCHAR(22) NOT NULL,
    PRIMARY KEY (user_id, tip_id),
    FOREIGN KEY (user_id) REFERENCES user_account(user_id),
    FOREIGN KEY (tip_id) REFERENCES tip(tip_id)
); 