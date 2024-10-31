SELECT e.name, e.salary, (e.salary * 100.0 / SUM(e.salary) OVER (PARTITION BY e.department)) AS salary_percentage FROM employees e order by salary_percentage
