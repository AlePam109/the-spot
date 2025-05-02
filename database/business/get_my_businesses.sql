SELECT business_id, name, address, is_open, stars
FROM business
WHERE business_account_id = %s;