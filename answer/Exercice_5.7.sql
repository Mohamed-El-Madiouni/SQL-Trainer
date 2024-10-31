SELECT * FROM employees WHERE salary <> (SELECT salary FROM employees WHERE id = 1) order by id
