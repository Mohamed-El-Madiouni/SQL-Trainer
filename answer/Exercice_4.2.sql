SELECT e.name, e.salary, RANK() OVER (PARTITION BY e.department ORDER BY e.salary DESC) AS salary_rank FROM employees e order by name
