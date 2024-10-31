SELECT e.name, e.salary, AVG(e.salary) OVER (PARTITION BY e.department) AS avg_department_salary FROM employees e order by name
