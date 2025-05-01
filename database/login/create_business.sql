BEGIN;

-- Check if the username already exists
SELECT account_id
FROM business_account
WHERE username = %s;

-- If not, insert the new business account
INSERT INTO business_account (name, username, password, business_count)
SELECT %s, %s, %s, 0
WHERE NOT EXISTS (
    SELECT 1 FROM business_account WHERE username = %s
)
RETURNING account_id;

COMMIT;
