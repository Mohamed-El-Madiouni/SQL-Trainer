SELECT e.name, e.salary, SUM(e.salary) OVER (ORDER BY e.salary) AS cumulative_salary FROM employees e order by salary
