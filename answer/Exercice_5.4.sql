with AvgSalIT as (
    SELECT AVG(salary) FROM department 
inner join employees on department.id = department
WHERE department_name = 'IT'
)

SELECT * FROM employees WHERE salary > (select * from AvgSalIT) order by salary
