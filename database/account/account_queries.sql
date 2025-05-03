-- Get user profile
SELECT user_id, username, name, yelping_since
FROM yelp_user
WHERE user_id = %s;

-- Update user profile
UPDATE yelp_user
SET name = %s
WHERE user_id = %s
RETURNING user_id;

-- Change password
UPDATE yelp_user
SET password = %s
WHERE user_id = %s AND password = %s
RETURNING user_id;

-- Delete account
DELETE FROM yelp_user
WHERE user_id = %s
RETURNING user_id;

-- Get user reviews
SELECT r.review_id, r.stars, r.text, r.date,
       b.name as business_name
FROM review r
JOIN business b ON r.business_id = b.business_id
WHERE r.user_id = %s
ORDER BY r.date DESC;

-- Get user tips
SELECT t.tip_id, t.text, t.date, t.compliment_count,
       b.name as business_name
FROM tip t
JOIN business b ON t.business_id = b.business_id
WHERE t.user_id = %s
ORDER BY t.date DESC; 