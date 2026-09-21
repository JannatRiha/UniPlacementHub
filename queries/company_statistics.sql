SELECT
    c.company_name,
    COUNT(DISTINCT p.id) AS total_postings,
    COUNT(a.id) AS total_applicants,
    COUNT(*) FILTER (WHERE a.status = 'selected') AS total_selected,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE a.status = 'selected')
        / NULLIF(COUNT(a.id), 0),
        2
    ) AS selection_rate
FROM companies_company c
LEFT JOIN postings_posting p ON p.company_id = c.user_id
LEFT JOIN applications_application a ON a.posting_id = p.id
GROUP BY c.user_id, c.company_name
ORDER BY total_applicants DESC;
