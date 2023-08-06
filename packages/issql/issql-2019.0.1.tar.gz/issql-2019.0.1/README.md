This is a simple library to check if a string is a reserved keyword in sql. 

It currently supports keywords from
* postgresql_10, 
* postgresql_8.1
* sql_2003
* sql_1999
* sql_92.

Usage, defaults to PostgreSQL 10

```python
import issql

issql.reserved('ALL')
>> True

issql.reserved('YES') 
>> False

issql.reserved('ABS') 
>>False

issql.reserved('ABS', version='sql_2003') 
>>True
```