-- Search businesses by name and location
SELECT b.business_id, b.name, b.address, b.city, b.state, b.stars, b.review_count, b.is_open
FROM business b
WHERE (
    LOWER(b.name) LIKE LOWER(%s) OR
    LOWER(b.categories) LIKE LOWER(%s)
) AND (
    LOWER(b.city) LIKE LOWER(%s) OR
    LOWER(b.state) LIKE LOWER(%s)
)
ORDER BY b.stars DESC, b.review_count DESC; 