SELECT * FROM employees e WHERE salary < (SELECT AVG(salary) FROM employees WHERE department =e.department) order by salary
