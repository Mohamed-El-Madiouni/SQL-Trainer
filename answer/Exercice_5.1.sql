with avg_salary as (
    SELECT AVG(salary) FROM employees
)
SELECT * FROM employees WHERE salary > (SELECT * FROM avg_salary) order by salary
