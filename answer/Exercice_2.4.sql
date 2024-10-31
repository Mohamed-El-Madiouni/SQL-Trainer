SELECT d.department_name, e.name FROM department d LEFT JOIN employees e ON d.id = e.department order by d.department_name
