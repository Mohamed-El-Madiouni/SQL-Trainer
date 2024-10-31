SELECT e.name, e.salary, e.salary - AVG(e.salary) OVER (PARTITION BY e.department) AS salary_difference FROM employees e order by salary_difference
