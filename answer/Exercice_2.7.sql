SELECT d.department_name, COUNT(e.id) AS young_employee_count FROM department d LEFT JOIN employees e ON d.id = e.department WHERE e.age < 30 GROUP BY d.department_name order by d.department_name
