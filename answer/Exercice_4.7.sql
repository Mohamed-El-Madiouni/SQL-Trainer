SELECT e.name, e.salary FROM employees e QUALIFY e.salary > AVG(e.salary) OVER (PARTITION BY e.department) order by salary
