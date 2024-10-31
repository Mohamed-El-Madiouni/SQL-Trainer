SELECT d.department_name, COUNT(e.id) AS employee_count FROM department d LEFT JOIN employees e ON d.id = e.department GROUP BY d.department_name order by d.department_name
