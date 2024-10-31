SELECT e.name FROM employees e JOIN department d ON e.department = d.id WHERE d.department_name = 'IT' order by name
