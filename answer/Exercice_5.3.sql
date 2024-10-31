WITH DepartmentEmployeeCount AS (
    SELECT department, COUNT(*) AS employee_count
    FROM employees
    GROUP BY department
)
SELECT d.department_name
FROM DepartmentEmployeeCount dec
JOIN department d ON dec.department = d.id
ORDER BY dec.employee_count DESC
LIMIT 1;
