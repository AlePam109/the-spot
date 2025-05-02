INSERT INTO business (
    business_id, name, address, city, state, postal_code,
    latitude, longitude, stars, review_count, is_open,
    attributes, categories, hours, business_account_id
)
VALUES (
    %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s
);