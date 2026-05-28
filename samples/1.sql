SELECT 
    department,
    AVG(salary) AS avg_salary,
    SUM(bonus) AS total_bonus,
    COUNT(*) AS employee_count
FROM employee_data
WHERE salary > 50000
GROUP BY department
ORDER BY department
LIMIT 10;