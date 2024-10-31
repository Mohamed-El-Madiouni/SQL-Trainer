SELECT d.department_name FROM department d JOIN employees e ON d.id = e.department GROUP BY d.department_name ORDER BY AVG(e.salary) DESC LIMIT 1
