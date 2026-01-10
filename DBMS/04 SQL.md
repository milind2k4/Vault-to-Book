Links: [[02 Relational Data Model]]
___
# SQL (Structured Query Language)

SQL is the standard language for interacting with Relational Database Management Systems (RDBMS). It is **Declarative** (you specify _what_ you want, not _how_ to get it).

## SQL Command Categories

| Category | Full Form                    | Commands                               | Purpose                                         |
| :------- | :--------------------------- | :------------------------------------- | :---------------------------------------------- |
| **DDL**  | Data Definition Language     | `CREATE`, `ALTER`, `DROP`, `TRUNCATE`  | Defines the structure (Schema). Auto-committed. |
| **DML**  | Data Manipulation Language   | `INSERT`, `UPDATE`, `DELETE`, `SELECT` | Manipulates data. Requires commit.              |
| **DCL**  | Data Control Language        | `GRANT`, `REVOKE`                      | Manages access rights/permissions.              |
| **TCL**  | Transaction Control Language | `COMMIT`, `ROLLBACK`, `SAVEPOINT`      | Manages transactions (ACID).                    |

## DDL (Data Definition Language)

### CREATE

Creates a new table or object.

```sql
CREATE TABLE Student (
    ID INT PRIMARY KEY,
    Name VARCHAR(50) NOT NULL,
    GPA DECIMAL(3, 2) CHECK (GPA >= 0.0)
);
```

### ALTER

Modifies the structure of an existing table.

```sql
ALTER TABLE Student ADD Email VARCHAR(100); -- Add Column
ALTER TABLE Student DROP COLUMN Email;      -- Remove Column
ALTER TABLE Student MODIFY Name VARCHAR(100); -- Change Data Type
```

### DROP vs TRUNCATE

- **DROP**: Removes the table structure AND data. Irreversible.
  - _Analogy_: Burning down the house.
- **TRUNCATE**: Removes all data but keeps the structure. Faster than DELETE. Cannot be rolled back.
  - _Analogy_: Removing all furniture but keeping the house.

## DML (Data Manipulation Language)

### SELECT (The Core)

Retrieves data.
**Execution Order**: `FROM` $\rightarrow$ `WHERE` $\rightarrow$ `GROUP BY` $\rightarrow$ `HAVING` $\rightarrow$ `SELECT` $\rightarrow$ `ORDER BY`.

```sql
SELECT Name, GPA
FROM Student
WHERE GPA > 3.5
ORDER BY GPA DESC;
```

### INSERT, UPDATE, DELETE

```sql
-- INSERT
INSERT INTO Student (ID, Name) VALUES (1, 'John');

-- UPDATE
UPDATE Student SET GPA = 4.0 WHERE ID = 1;

-- DELETE
DELETE FROM Student WHERE GPA < 2.0;
```

## Advanced Querying

### Aggregate Functions

Functions that perform a calculation on a set of values and return a single value.

`COUNT()`
- `COUNT(*)`: counts the total number of rows.
- `COUNT(column_name)`: counts no. of non-null values in that column.

The following are numeric functions (they all ignore NULL values):
- `SUM()` sums the values of a column.
- `AVG()` finds average of a numeric attribute.
- `MAX()` finds the max.
- `MIN()` finds the min.

#### Other Functions (Numeric)

- `CEIL()` returns the smallest integer larger than the input fraction.
- `FLOOR()` returns the largest integer smaller than the input fraction.
- `ROUND(number, round_place)` rounds the number
    - after the decimal if round_place > 0 e.g. `ROUND(15.44, 1) = 15.4`
    - before the decimal if round_place < 0 e.g. `ROUND(14.999, -1) = 10`
- `LN()`
- `LOG(base, number)`
- `POWER(base, exp)`
- `SQRT()`
- `SIGN()`
- `ABS()`
- `MOD(num, div)` returns remainder after dividing num by div.
- `SIN(), COS(), TAN()` take input in radians.
- `TRUNC(number, places)` removes numbers after decimal.

Using numeric functions on non-numeric data types will give an error.

#### Non Numeric Functions (String)

- `ASCII()`
- `CHR(ascii_value)`
- `CONCAT(string1, string2)` or `string1 || string2`
- `INITCAP(string)` returns string after converting first letter of each word to capital.
- `LOWER()`
- `UPPER()`
- `LPAD(string1, n, string2)` returns string left-padded to length n with characters from string2.
- `RPAD()`
- `LTRIM(string1, [string2])` removes leading characters (default: spaces, or chars in `string2`) from `string1`.
- `RTRIM()`
- `REPLACE(string1, to_be_replaced, replacement)` replaces all instances of `to_be_replaced` with `replacement`.
- `SOUNDEX(string)` returns a character string containing the phonetic representation of string. This functions allows your to compare worlds that are spelled differently but sound the same.

    ```sql
    SELECT ename from emp WHERE SOUNDEX(ename) = SOUNDEX('SMYTHE');
    
    gives,
    SMITH
    ```

#### Date Functions

- `SYSDATE`: Returns the current system date and time.
- `ADD_MONTHS(date, n)`: Adds `n` months to a date.
- `MONTHS_BETWEEN(date1, date2)`: Returns number of months between two dates.
- `TO_DATE(string, format)`: Converts a string to a DATE value.
- `TO_CHAR(date, format)`: Converts a DATE value to a string.

### GROUP BY and HAVING

- **GROUP BY**: Groups rows that have the same values into summary rows.
- **HAVING**: Filters groups (like `WHERE` filters rows).

> [!TIP] > **Analogy**
> - **WHERE:** The bouncer at the club entrance checking IDs (filters individuals).
> - **GROUP BY:** Organizing people into tables based on their shirt color.
> - **HAVING:** The waiter checking which tables have more than 5 people (filters groups).

```sql
SELECT Dept, AVG(Salary)
FROM Employee
GROUP BY Dept
HAVING AVG(Salary) > 50000;
```

## [[4.5 Joins]]

### Union, Intersect and Minus

These are set operators that combine the results of two `SELECT` statements. The result sets must be "union-compatible" (same number of columns, and compatible data types).

- `UNION`: Returns all unique rows from both queries.
- `UNION ALL`: Returns all rows from both queries, including duplicates.
- `INTERSECT`: Returns only the rows that appear in both query results.
- `MINUS` (Oracle) or `EXCEPT` (Standard SQL): Returns rows from the first query that are not in the second query.

```sql
-- Get a list of all unique department IDs present in either table
SELECT did FROM emp
UNION
SELECT did FROM dept;
```

## Subqueries

A query nested inside another query.

### Nested Subquery

The inner query executes once, and its result is used by the outer query.

```sql
-- Find students with GPA higher than the average
SELECT Name FROM Student
WHERE GPA > (SELECT AVG(GPA) FROM Student);
```

### Correlated Subquery

The inner query depends on the outer query and executes **once for every row** processed by the outer query. **Performance Heavy**.

```sql
-- Find employees earning more than the average of THEIR department
SELECT Name, Salary, DeptID FROM Employee E1
WHERE Salary > (
    SELECT AVG(Salary) FROM Employee E2
    WHERE E2.DeptID = E1.DeptID -- Correlation
);
```