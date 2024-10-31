SELECT e.name, e.salary, LAG(e.salary) OVER (ORDER BY e.salary) AS previous_salary FROM employees e order by salary
