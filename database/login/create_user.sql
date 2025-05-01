BEGIN;

-- Check for existing username
SELECT user_id
FROM yelp_user
WHERE username = %s;

-- If no match, insert new user
INSERT INTO yelp_user (name, username, password, yelping_since)
SELECT %s, %s, %s, CURRENT_DATE
WHERE NOT EXISTS (
    SELECT 1 FROM yelp_user WHERE username = %s
)
RETURNING user_id;

COMMIT;
