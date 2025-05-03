-- Insert a new review
INSERT INTO review (review_id, user_id, business_id, stars, text)
VALUES (%s, %s, %s, %s, %s)
RETURNING review_id;

-- Get reviews for a business
SELECT r.review_id, r.stars, r.text, r.useful, r.funny, r.cool, r.date,
       u.username, u.name as user_name
FROM review r
JOIN yelp_user u ON r.user_id = u.user_id
WHERE r.business_id = %s
ORDER BY r.date DESC;

-- Add a reaction to a review
INSERT INTO review_reaction (user_id, review_id, reaction_type)
VALUES (%s, %s, %s)
ON CONFLICT (user_id, review_id, reaction_type) DO NOTHING;

-- Update review reaction counts
UPDATE review
SET useful = (SELECT COUNT(*) FROM review_reaction WHERE review_id = %s AND reaction_type = 'useful'),
    funny = (SELECT COUNT(*) FROM review_reaction WHERE review_id = %s AND reaction_type = 'funny'),
    cool = (SELECT COUNT(*) FROM review_reaction WHERE review_id = %s AND reaction_type = 'cool')
WHERE review_id = %s;

-- Insert a new tip
INSERT INTO tip (tip_id, user_id, business_id, text)
VALUES (%s, %s, %s, %s)
RETURNING tip_id;

-- Get tips for a business
SELECT t.tip_id, t.text, t.compliment_count, t.date,
       u.username, u.name as user_name
FROM tip t
JOIN yelp_user u ON t.user_id = u.user_id
WHERE t.business_id = %s
ORDER BY t.date DESC;

-- Add a praise to a tip
INSERT INTO tip_praise (user_id, tip_id)
VALUES (%s, %s)
ON CONFLICT (user_id, tip_id) DO NOTHING;

-- Update tip compliment count
UPDATE tip
SET compliment_count = (SELECT COUNT(*) FROM tip_praise WHERE tip_id = %s)
WHERE tip_id = %s; 