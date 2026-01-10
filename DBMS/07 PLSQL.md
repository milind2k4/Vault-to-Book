Links: [[03 SQL]]

---

# PL/SQL (Procedural Language extensions to SQL)

PL/SQL combines the data manipulation power of SQL with the processing power of procedural languages (Loops, Conditions, Variables).

## Block Structure

The basic unit of a PL/SQL program.

```sql
DECLARE
    -- Variables, Cursors, Types
    v_salary NUMBER;
BEGIN
    -- SQL Statements, Logic
    SELECT salary INTO v_salary FROM Emp WHERE ID = 1;
EXCEPTION
    -- Error Handling
    WHEN NO_DATA_FOUND THEN
        DBMS_OUTPUT.PUT_LINE('No Employee Found');
END;
/
```

## Variables & Data Types

### Scalar Types

Single values (e.g., `NUMBER`, `VARCHAR2`, `DATE`, `BOOLEAN`).

### Attributes (%TYPE and %ROWTYPE)

- **`%TYPE`**: Declares a variable with the _same type_ as a table column.
  ```sql
  v_name Emp.Name%TYPE; -- If Emp.Name is VARCHAR2(50), v_name becomes VARCHAR2(50)
  ```
- **`%ROWTYPE`**: Declares a record variable that matches the _entire row_ structure of a table.
  ```sql
  v_emp Emp%ROWTYPE;
  -- Access fields: v_emp.Name, v_emp.Salary
  ```

## Control Structures

### Conditional Logic

**IF-THEN-ELSIF-ELSE**

```sql
IF v_score >= 90 THEN
    DBMS_OUTPUT.PUT_LINE('A');
ELSIF v_score >= 80 THEN
    DBMS_OUTPUT.PUT_LINE('B');
ELSE
    DBMS_OUTPUT.PUT_LINE('C');
END IF;
```

**CASE Statement**

```sql
CASE grade
    WHEN 'A' THEN DBMS_OUTPUT.PUT_LINE('Excellent');
    WHEN 'B' THEN DBMS_OUTPUT.PUT_LINE('Good');
    ELSE DBMS_OUTPUT.PUT_LINE('Average');
END CASE;
```

### Loops

**Basic Loop**

```sql
LOOP
    i := i + 1;
    EXIT WHEN i > 5;
END LOOP;
```

**WHILE Loop**

```sql
WHILE i <= 5 LOOP
    i := i + 1;
END LOOP;
```

**FOR Loop**

```sql
FOR i IN 1..5 LOOP
    DBMS_OUTPUT.PUT_LINE(i);
END LOOP;
```

## Cursors

A pointer to a memory area (Context Area) that stores the result of a SQL statement.

### Implicit Cursor

Automatically created for `INSERT`, `UPDATE`, `DELETE`, and single-row `SELECT INTO`.

- **Attributes**:
  - `%FOUND`: True if row affected.
  - `%NOTFOUND`: True if no row affected.
  - `%ROWCOUNT`: Number of rows affected.

### Explicit Cursor

Defined by the programmer for queries returning **multiple rows**.
**Steps**:

1.  **DECLARE**: `CURSOR c1 IS SELECT * FROM Emp;`
2.  **OPEN**: `OPEN c1;` (Allocates memory).
3.  **FETCH**: `FETCH c1 INTO v_emp;` (Retrieves one row).
4.  **CLOSE**: `CLOSE c1;` (Releases memory).

> [!EXAMPLE] > Explicit Cursor to Print Employee Names
>
> ```sql
> DECLARE
>     CURSOR c_emp IS SELECT Name, Salary FROM Emp;
>     v_name Emp.Name%TYPE;
>     v_sal  Emp.Salary%TYPE;
> BEGIN
>     OPEN c_emp;
>     LOOP
>         FETCH c_emp INTO v_name, v_sal;
>         EXIT WHEN c_emp%NOTFOUND;
>         DBMS_OUTPUT.PUT_LINE(v_name || ' earns ' || v_sal);
>     END LOOP;
>     CLOSE c_emp;
> END;
> /
> ```

## Procedures vs Functions

| Feature          | Procedure                                   | Function                                              |
| :--------------- | :------------------------------------------ | :---------------------------------------------------- |
| **Return Value** | Optional (using `OUT` parameters).          | **Must** return a value.                              |
| **Usage**        | Executed as a statement (`EXEC proc_name`). | Called as part of an expression (`v := func_name()`). |
| **DML**          | Can execute DML (Insert/Update).            | Can execute DML (but restricted inside SELECT).       |

> [!Example]
>
> ```sql
> CREATE PROCEDURE UpdateSal(p_id IN INT, p_amount IN INT) IS
> BEGIN
>     UPDATE Emp SET Salary = Salary + p_amount WHERE ID = p_id;
>     COMMIT;
> END;
> /
> ```

## Triggers

Stored programs automatically fired (executed) in response to events (`INSERT`, `UPDATE`, `DELETE`).

### Types

1.  **Row-Level**: Fires once for _each row_ affected. (Uses `FOR EACH ROW`).
2.  **Statement-Level**: Fires once for the _entire SQL statement_ (even if 100 rows are updated).
3.  **Timing**: `BEFORE` or `AFTER`.

> [!Example] > Audit
>
> ```sql
> CREATE TRIGGER Audit_Emp
> AFTER UPDATE OF Salary ON Emp
> FOR EACH ROW
> BEGIN
>     INSERT INTO Emp_Audit (ID, Old_Sal, New_Sal, Date)
>     VALUES (:OLD.ID, :OLD.Salary, :NEW.Salary, SYSDATE);
> END;
> /
> ```

- `:NEW`: Access values _after_ the update/insert.

## Exception Handling

Errors in PL/SQL are called Exceptions.

### Predefined Exceptions

- `NO_DATA_FOUND`: SELECT INTO returns no rows.
- `TOO_MANY_ROWS`: SELECT INTO returns more than one row.
- `ZERO_DIVIDE`: Division by zero.
- `DUP_VAL_ON_INDEX`: Unique constraint violation.

### User-Defined Exceptions

Declared by the programmer and raised explicitly.

```sql
DECLARE
    e_invalid_age EXCEPTION;
    v_age NUMBER := 15;
BEGIN
    IF v_age < 18 THEN
        RAISE e_invalid_age;
    END IF;
EXCEPTION
    WHEN e_invalid_age THEN
        DBMS_OUTPUT.PUT_LINE('Error: Age must be 18+');
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Unknown Error: ' || SQLERRM);
END;
/
```

## Dynamic SQL
Used to execute SQL statements that are constructed at runtime (e.g., DDL statements inside PL/SQL).

```sql
BEGIN
    EXECUTE IMMEDIATE 'CREATE TABLE Temp_Table (ID INT)';
END;
/
```
