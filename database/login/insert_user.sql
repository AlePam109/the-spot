INSERT INTO yelp_user (user_id, name, username, password, yelping_since)
SELECT %s, %s, %s, %s, CURRENT_DATE
WHERE NOT EXISTS (
    SELECT 1 FROM yelp_user WHERE username = %s
)
RETURNING user_id;
