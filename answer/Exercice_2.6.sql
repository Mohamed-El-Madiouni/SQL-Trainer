SELECT e.name, d.department_name FROM employees e JOIN department d ON e.department = d.id WHERE e.age > 30 order by name
