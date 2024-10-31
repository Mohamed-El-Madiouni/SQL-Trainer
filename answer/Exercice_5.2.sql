with avg_sal_sup_sixty as (
    SELECT department
    FROM employees
    GROUP BY department
    HAVING AVG(salary) > 60000
)
SELECT department_name
FROM department
WHERE id IN (
    SELECT * from avg_sal_sup_sixty
) order by department_name desc