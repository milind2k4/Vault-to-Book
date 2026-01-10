

# DBMS {#dbms}

\etocsettocstyle{\textbf{Chapter Contents}\par\rule{\linewidth}{0.5pt}}{\par\rule{\linewidth}{0.5pt}}
\localtableofcontents
\noindent


## Fundamental Concepts
### Data vs. Information

- **Data**: Raw, unprocessed facts and figures without context.
  - _Example_: `100`, `Red`, `John`.
- **Information**: Processed data that has meaning and context.
  - _Example_: "John scored 100 marks in the Red team."

### Database Management System (DBMS)

A **DBMS** is a general-purpose software system that facilitates the process of defining, constructing, manipulating, and sharing databases among various users and applications.

> [!TIP] > **Analogy** 
> Think of a **Database** as a library full of books (data). The **DBMS** is the librarian who manages the catalog, organizes the books, ensures security, and helps you find exactly what you need. You don't go to the shelf yourself; you ask the librarian.

### Database System vs. File System

Before DBMS, data was stored in OS files (File Processing System).

| Feature         | File System                                                                                               | DBMS                                                    |
| :-------------- | :-------------------------------------------------------------------------------------------------------- | :------------------------------------------------------ |
| **Structure**   | Unstructured or ad-hoc formats.                                                                           | Structured (Schema-defined).                            |
| **Redundancy**  | **High:** Same data repeated in multiple files (e.g., Student address in 'Library' and 'Accounts' files). | **Controlled:** Normalization minimizes duplication.    |
| **Consistency** | **Low:** Updating address in 'Library' might leave 'Accounts' with old data (Data Inconsistency).         | **High:** Changes are propagated or shared.             |
| **Isolation**   | **Low:** Data is scattered; formats vary. Hard to write new apps.                                         | **High:** Data Independence separates app from storage. |
| **Atomicity**   | **No:** If a transfer fails halfway, money is lost.                                                       | **Yes:** Transactions are all-or-nothing (ACID).        |
| **Security**    | OS-level (File permissions).                                                                              | Granular (Table/Row/Column level).                      |
| **Concurrency** | **Poor:** OS locks entire files.                                                                          | **High:** Fine-grained locking (Row-level).             |

## Database Architecture

### Three-Schema Architecture

Proposed by ANSI/SPARC to achieve **Data Independence**. It separates the user view from the physical storage.

![\ ](images/mermaid_b9c9351ddd0fc57ce753a9e2012f2ef8.png){height=11cm}

1.  **External Level (View Level)**:
    - Describes **part** of the database relevant to a specific user.
    - _Example_: A Student sees `Grades`, but not `FacultySalary`.
2.  **Conceptual Level (Logical Level)**:
    - Describes **what** data is stored and relationships. Hides physical details.
    - _Example_: `Student(ID, Name, Age)` table definition.
3.  **Internal Level (Physical Level)**:
    - Describes **how** data is stored (block size, compression, indexes, hashing).
    - _Example_: "Stored as a B+ Tree on Drive D:".

### Data Independence

The capacity to change the schema at one level of a database system without having to change the schema at the next higher level.

#### Logical Data Independence

- **Definition**: Ability to change the **Conceptual Schema** without affecting **External Schemas** (Application Programs).
- **Scenario**: Adding a new column `DateOfBirth` to the `Student` table.
- **Result**: Existing apps that only read `Name` and `ID` **do not crash**. They simply ignore the new column.
- **Analogy**: A restaurant changes its kitchen layout (Conceptual). The menu (External) remains the same for the customer.

#### Physical Data Independence

- **Definition**: Ability to change the **Internal Schema** without affecting the **Conceptual Schema**.
- **Scenario**: Creating a new **Index** on `Student(ID)` for faster search, or moving data from HDD to SSD.
- **Result**: The logical table structure (`CREATE TABLE`) remains exactly the same. The query runs faster, but the query _code_ doesn't change.
- **Analogy**: The library moves books from wooden shelves to metal shelves (Physical). The catalog numbers (Conceptual) and how you search for books (External) remain unchanged.

## DBMS Architecture Styles

### 2-Tier Architecture (Client-Server)

- **Client**: Runs the application and UI. Communicates directly with the DB.
- **Server**: Runs the DBMS.
- **Drawback**: Security risk (direct DB access), poor scalability.
- **Use Case**: JDBC/ODBC applications.

### 3-Tier Architecture (Web Applications)

- **Client**: Web Browser (Presentation Layer).
- **Application Server**: Business Logic (Java/Spring, Node.js).
- **Database Server**: DBMS (Data Layer).
- **Flow**: Client $\leftrightarrow$ App Server $\leftrightarrow$ DB Server.
- **Benefit**: Enhanced security (Client never touches DB directly), scalability.

## Database Users & Administrators

| Role                             | Responsibilities                                                                      |
| :------------------------------- | :------------------------------------------------------------------------------------ |
| **Database Administrator (DBA)** | Superuser. Manages schema, security, backups, performance tuning, and user access.    |
| **Application Programmer**       | Writes code (Java, Python) to interact with the DB using DML queries.                 |
| **Sophisticated User**           | Analysts/Scientists who write complex SQL queries/scripts for data mining.            |
| **Naive User**                   | End-users accessing DB via GUI (e.g., Bank teller using a form). They don't know SQL. |

## Data Models

A collection of conceptual tools for describing data, relationships, semantics, and constraints.

1.  **Relational Model**: Uses **Tables** (Relations). Current standard. (SQL).
2.  **Entity-Relationship (ER) Model**: High-level design model using **Entities** and **Relationships**. (Diagrams).
3.  **Object-Based Model**: Extends ER with OOP concepts (Encapsulation, Methods).
4.  **Semistructured Model**: Data with flexible structure (XML, JSON).


\newpage



# Entity Relation Diagram {#entity-relation-diagram}

\etocsettocstyle{\textbf{Chapter Contents}\par\rule{\linewidth}{0.5pt}}{\par\rule{\linewidth}{0.5pt}}
\localtableofcontents
\noindent


The **ER Model** is a high-level conceptual data model used to define the data elements and relationships for a specified system. It develops a conceptual design for the database.

### Entity

An object in the real world that is distinguishable from other objects.

- **Entity Set**: A set of entities of the same type that share the same properties.
  - _Example_: Set of all persons, companies, trees, holidays.
- **Strong Entity**: An entity that has a primary key. Represented by a **single rectangle**.
- **Weak Entity**: An entity that cannot be uniquely identified by its own attributes alone. It must be associated with a _Strong Entity_ (Owner Entity). Represented by a **double rectangle**.
  - _Discriminator (Partial Key)_: Attributes that distinguish weak entities within the owner entity set. Dashed underline.

### Attributes

Properties used to describe an entity.

- **Simple**: Atomic values (e.g., `Age`).
- **Composite**: Can be divided into sub-parts (e.g., `Name` $\rightarrow$ `FirstName`, `LastName`).
- **Multi-valued**: Can have multiple values for a single entity (e.g., `PhoneNumbers`). **Double Ellipse**.
- **Derived**: Value is derived from other attributes (e.g., `Age` from `DOB`). **Dashed Ellipse**.

### Relationships

An association among several entities.

- **Degree**: Number of entity sets participating in a relationship.
  - _Unary_ (Recursive): Person _married to_ Person.
  - _Binary_: Student _enrolls in_ Course.
  - _Ternary_: Employee _works on_ Project _using_ Skill.
- **Cardinality Ratios**: Expresses the number of entities to which another entity can be associated.
  - **1:1**: One student has one ID card.
  - **1:N**: One department has many employees.
  - **M:N**: Many students enroll in many courses.
- **Participation Constraints**:
  - **Total Participation** (Double Line): Every entity in the set _must_ participate (e.g., Every Loan must belong to a Customer).
  - **Partial Participation** (Single Line): Some entities may not participate.

## Keys

A **Key** is a set of attributes that uniquely identifies an entity in an entity set.

1.  **Super Key**: A set of one or more attributes that, taken collectively, allows us to identify uniquely an entity in the entity set.
    - _Example_: `{ID}`, `{ID, Name}`, `{ID, Phone}`.
2.  **Candidate Key**: A **minimal** super key. If any attribute is removed, it is no longer a super key.
    - _Example_: `{ID}` is minimal. `{ID, Name}` is not (remove Name, ID is still unique).
3.  **Primary Key**: The candidate key chosen by the database designer as the principal means of identifying entities.
    - _Constraint_: Cannot be NULL.

## Reduction of ER Diagram to Relational Tables

This is the algorithm to convert a conceptual ER design into a logical Relational Schema.

#### Step 1: Strong Entity Sets

Create a table for each strong entity.

- **Columns**: All simple attributes.
- **PK**: The primary key of the entity.

#### Step 2: Weak Entity Sets

Create a table for the weak entity $W$ with owner $E$.

- **Columns**: Attributes of $W$ + Primary Key of $E$ (as Foreign Key).
- **PK**: Composite Key $\{ \text{PK of } E, \text{Discriminator of } W \}$.
- **Constraint**: `ON DELETE CASCADE` (usually).

#### Step 3: 1:1 Relationship

- **Option A (Foreign Key)**: Add the PK of one side as a FK to the other side. Prefer adding to the side with **Total Participation** to avoid NULLs.
- **Option B (Merged)**: If both sides have total participation, merge them into a single table.

#### Step 4: 1:N Relationship

- **Rule**: Take the PK of the "1" side and add it as a Foreign Key to the "N" side table.
- _Example_: `Dept (1) ---- (N) Employee`. Add `DeptID` to `Employee` table.

#### Step 5: M:N Relationship

Create a new **Junction Table** (Relationship Table).

- **Columns**: PK of Entity A + PK of Entity B + Attributes of the relationship itself.
- **PK**: Composite Key $\{ \text{PK of A}, \text{PK of B} \}$.

#### Step 6: Multi-valued Attributes

Create a new table for the attribute.

- **Columns**: PK of the Entity + The Attribute Value.
- **PK**: Composite Key $\{ \text{PK of Entity}, \text{Attribute Value} \}$.

## Case Study: Banking System

### Scenario

- **Bank** has multiple **Branches**.
- **Customers** open **Accounts** at a branch.
- **Customers** take **Loans** from a branch.
- **Employees** work for a branch.
- **Customer** can have multiple **Addresses** (Multi-valued).
- **Loan** is a Weak Entity dependent on Branch (conceptually, though often modeled as strong in practice, let's assume weak for this example).

### ER Design

1.  **Entities**: `Branch`, `Customer`, `Account`, `Loan`, `Employee`.
2.  **Relationships**:
    - `Branch` (1) --- (N) `Loan` (Weak).
    - `Customer` (M) --- (N) `Account` (_Depositor_).
    - `Customer` (M) --- (N) `Loan` (_Borrower_).
    - `Branch` (1) --- (N) `Account`.

### Reduction to Tables

1.  **Branch** (Strong Entity)
    - `Branch(BranchName, BranchCity, Assets)`
    - **PK**: `BranchName`

2.  **Customer** (Strong Entity)
    - `Customer(CustID, CustName, CustStreet, CustCity)`
    - **PK**: `CustID`

3.  **Customer_Phone** (Multi-valued Attribute)
    - `Cust_Phone(CustID, PhoneNumber)`
    - **FK**: `CustID` ref `Customer`
    - **PK**: `{CustID, PhoneNumber}`

4.  **Account** (Strong Entity + 1:N from Branch)
    - `Account(AccNumber, Balance, BranchName)`
    - **FK**: `BranchName` ref `Branch`
    - **PK**: `AccNumber`

5.  **Loan** (Weak Entity + 1:N from Branch)
    - `Loan(LoanNumber, Amount, BranchName)`
    - **FK**: `BranchName` ref `Branch`
    - **PK**: `LoanNumber` (Assuming LoanNumber is unique globally, else `{BranchName, LoanNumber}`)

6.  **Depositor** (M:N Relationship between Customer and Account)
    - `Depositor(CustID, AccNumber)`
    - **FK**: `CustID` ref `Customer`, `AccNumber` ref `Account`
    - **PK**: `{CustID, AccNumber}`

7.  **Borrower** (M:N Relationship between Customer and Loan)
    - `Borrower(CustID, LoanNumber)`
    - **FK**: `CustID` ref `Customer`, `LoanNumber` ref `Loan`
    - **PK**: `{CustID, LoanNumber}`

> [!TIP] > **Analogy for Reduction**
> - **1:N** is like a Parent-Child relationship. The Child (N side) carries the Parent's name (FK).
> - **M:N** is like a "Marriage" or "Partnership". You need a marriage certificate (Junction Table) that lists both partners.


\newpage



# Relational Data Model {#relational-data-model}

\etocsettocstyle{\textbf{Chapter Contents}\par\rule{\linewidth}{0.5pt}}{\par\rule{\linewidth}{0.5pt}}
\localtableofcontents
\noindent


The **Relational Model** (proposed by E.F. Codd, 1970) represents data as a collection of **relations** (tables). It is the theoretical basis for SQL.

## Definitions

### Relation ($R$)

Mathematically, a relation is a subset of the Cartesian product of a list of domains.

- **Table**: A visual representation of a relation.
- **Tuple ($t$)**: A row in the table. Represents a single entity instance.
- **Attribute ($A$)**: A column header. Represents a property of the entity.
- **Domain ($D$)**: The set of atomic values allowed for an attribute (e.g., Integer, String).

### Schema vs. Instance

- **Relation Schema ($R$)**: The logical design (blueprint).
  - Notation: $R(A_1, A_2, ..., A_n)$
  - _Example_: `Student(ID, Name, GPA)`
- **Relation Instance ($r$)**: The actual data (set of tuples) at a specific moment.
  - Notation: $r(R)$
  - _Property_: A relation is a **Set**, meaning **no duplicate tuples** are allowed and **order does not matter**.

#### Properties
1.  **Degree (Arity)**: The number of attributes (columns).
2.  **Cardinality**: The number of tuples (rows).

## Relational Keys
[[01 Entity Relation Diagram#Keys]]

A **Key** is a set of attributes used to uniquely identify a tuple.

### Hierarchy of Keys

1.  **Super Key ($SK$)**: A set of attributes that **uniquely identifies** a tuple.
    - _Condition_: For any two distinct tuples $t_1, t_2$, if $t_1[SK] = t_2[SK]$, then $t_1 = t_2$.
    - _Example_: `{ID}`, `{ID, Name}`, `{ID, Name, GPA}`.
2.  **Candidate Key ($CK$)**: A **minimal** Super Key.
    - _Condition_: It is a Super Key, and no proper subset of it is a Super Key.
    - _Example_: `{ID}` is a Candidate Key. `{ID, Name}` is NOT (because removing Name still leaves `{ID}`, which is unique).
3.  **Primary Key ($PK$)**: The Candidate Key chosen by the DBA to identify tuples.
    - _Constraint_: Cannot be NULL.
4.  **Alternate Key**: Candidate Keys that were _not_ chosen as Primary Key.
5.  **Foreign Key ($FK$)**: An attribute in one table that refers to the Primary Key of another table.

> [!TIP] > **Analogy**
> - **Super Key:** Any combination of ID cards that proves who you are (Passport + Driver's License + Library Card).
> - **Candidate Key:** Just _one_ ID card (Passport OR Driver's License).
> - **Primary Key:** The one you show at the airport (Passport).

## Integrity Constraints

Rules that maintain the quality and consistency of data.

#### Domain Constraints

Ensures that values for an attribute come from the defined domain.

- _Example_: `Age` must be an Integer $> 0$. `Name` cannot be an Image.

#### Entity Integrity Constraint

- **Rule**: The **Primary Key** cannot be **NULL**.
- **Reason**: The PK is the identity of the tuple. A NULL identity implies the entity doesn't exist or cannot be distinguished.

#### Referential Integrity Constraint

- **Rule**: A **Foreign Key** value must either:
  1.  Match an existing Primary Key value in the referenced relation.
  2.  Be NULL (if allowed).
- **Purpose**: Prevents **Dangling Pointers** (referencing non-existent data).

##### Handling Violations (ON DELETE / ON UPDATE)

When a referenced row (e.g., Department) is deleted, what happens to the referencing rows (e.g., Employees)?

1.  **Restrict / No Action**: Reject the delete. (Default).
2.  **Cascade**: Delete the referencing rows too. (Delete Dept $\rightarrow$ Delete all its Employees).
3.  **Set Null**: Set the FK to NULL. (Employee becomes "Department-less").
4.  **Set Default**: Set the FK to a default value.


## [[03 Relational Algebra]]

| Operation             |  Symbol  | Type   | Description                                  |
| :-------------------- | :------: | :----- | :------------------------------------------- |
| **Select**            | $\sigma$ | Unary  | Filters rows based on a condition.           |
| **Project**           |  $\pi$   | Unary  | Selects specific columns.                    |
| **Union**             |  $\cup$  | Binary | Combines tuples from two relations.          |
| **Set Difference**    |   $-$    | Binary | Tuples in A but not in B.                    |
| **Cartesian Product** | $\times$ | Binary | Combines every row of A with every row of B. |
| **Rename**            |  $\rho$  | Unary  | Renames a relation or attribute.             |


\newpage



# Relational Algebra {#relational-algebra}

\etocsettocstyle{\textbf{Chapter Contents}\par\rule{\linewidth}{0.5pt}}{\par\rule{\linewidth}{0.5pt}}
\localtableofcontents
\noindent


The algebra which can be performed on a relational database.

A relational db is expected to be equipped with a query language. This query language helps with the operations performed on an instance of db.

There are two types of query languages:
- **Relational Algebra:** A procedural query language. It has fixed syntax and semantics, with operators that are applied to relations (operands) to produce a new relation. It describes _how_ to get the result.
- **Relational Calculus:** A non-procedural or declarative query language. It describes _what_ result to get, but not the steps to get it.

The fundamental operations of relational algebra are grouped into unary (acting on one relation) and binary (acting on two relations) operations.

### Unary Relational Operations

#### Select ($\sigma$)

Selects a subset of tuples (rows) from a relation that satisfy a given predicate (condition). It acts like a `WHERE` clause in SQL.
$$\sigma_{p}(r)$$
where,
$r$ is relation
$p$ is predicate i.e. logic ("filter")

E.g.
$$\ce{ \sigma_{ subject = 'database' \ and \ price = 1000} (Books) }$$
$$\ce{ \sigma_{branch\_name ='Perryride'}(Loan) }$$
$$\ce{ \sigma_{Amount > 1000\  \wedge\ Branch\_name \neq 'Perryride'}(Loan) }$$

#### Project ($\Pi$)

Selects a subset of attributes (columns) from a relation. It automatically removes duplicate rows from the result, as relations are sets.

$$\Pi_{A1, A2, A3}(r)$$
where,
$A_{i}$ are attribute names and
$r$ is relation
E.g. To get only the name and duration from the Course table:
$$\ce{ \Pi_{Name, Duration}(Course) }$$

#### Rename ($\rho$)

Renames the output relation or its attributes. This is crucial for self-joins or for clarifying the results of complex expressions.
$$\rho_{x}( E)$$
where the result of expression E is saved with name $x$.
$$\rho_{x(A1, A2, ...)}( E)$$
where the result of expression E is saved as $x$, and its attributes are renamed to $A1, A2, ...$

### Binary Relational Operations
#### Set Theory Operations
These operations require the two relations ($r$ and $s$) to be **union-compatible** (or type-compatible):
1. They must have the same number of attributes (same degree/arity).
2. The domains of corresponding attributes must be the same.

- Union ($r\cup s$)
    Performs binary union. The result contains all tuples that are in $r$, or in $s$, or in both.
- Set Difference ($r - s$)
    The result contains all tuples that are in $r$ but not in $s$.
- Intersection ($r \cap s$)
    The result contains all tuples that are in both $r$ and $s$.
    (Note: This is a derived operator, as $r \cap s = r - (r - s)$)

#### Cartesian Product / Cross Product ($r \times s$)

Combines every tuple from $r$ with every tuple from $s$. If $r$ has $n$ tuples and $s$ has $m$ tuples, the result will have $n \times m$ tuples. The resulting relation has all attributes from both $r$ and $s$.

#### Join Operations

Joins are used to combine related tuples from two different relations into a single tuple.

##### Theta Join ($\bowtie_{\theta}$)
This is the most general join. It is equivalent to a Cartesian Product followed by a Select operation.
$$r \bowtie_{\theta} s = \sigma_{\theta}(r \times s)$$
Here, $\theta$ is a predicate (condition) that compares attributes from $r$ and $s$.
    
##### Equi Join
A special type of Theta Join where the predicate $\theta$ only uses the equality operator (=).

##### Natural Join ($r \bowtie s$)
This is the most common join. It is a subset of the Cartesian product.
1. It performs an Equi Join on _all_ attributes that have the _same name_ in both relations.
2. The result has all attributes of both tables, but the common attributes appear only once. 
It results in the set of all combinations of tuples where they have equal values for their common attributes.

E.g. $r(A, B, C)$ and $s(B, D)$. The natural join $r \bowtie s$ is:
$$\Pi_{r.A, r.B, r.C, s.D}(\sigma_{r.B = s.B}(r \times s))$$

#### Division ($\div$)

This operation is used for queries that include the phrase "for all".

Let relation $r$ have attributes $R$ and relation $s$ have attributes $S$, where $S$ is a subset of $R$.

The result of $r \div s$ will have attributes $R - S$.

It returns all tuples $t$ from the $R-S$ part of $r$ such that for _every_ tuple in $s$, the combined tuple $(t, s)$ exists in $r$.

**E.g. "Find students who have taken _all_ courses in the 'CS' department."**

1. $\ce{ AllStudentsAndCourses(StudentID, CourseID) }$
    
2. $\ce{ CS\_Courses(CourseID) = \Pi_{CourseID}(\sigma_{Dept\ =  \ 'CS'}(Course)) }$
    
3. $\ce{ Result(StudentID) = AllStudentsAndCourses \div CS\_Courses }$

### Queries in Relational Algebra

Given the following schema:
```
passenger(pid, pname, pgender, pcity)
agency(aid, aname, acity)
flight(fid, fdate, time, src, dest)
booking(pid, aid, fid, fdate)
```

Q: Find all flights to 'New Delhi'.
$$\ce{ \sigma_{dest\ =\ 'New Delhi'} (flight) }$$

Q: Find all flights from 'Chennai' to 'New Delhi'.
$$\ce{ \sigma_{src\ =\ 'Chennai'\ and\ dest\ =\ 'New Delhi'} (flight) }$$

**Q: Find only the flight numbers (fid) for passenger with pid '123' for flights to 'Chennai' before '06.11.2020'.**
- First, find the relevant flights:
    $$\ce{ F \leftarrow \sigma_{ dest\ =\  'Chennai'\ and\ fdate\ <\ '06.11.2020'}(flight) }$$
    
- Next, find the relevant bookings:
    $$\ce{ B \leftarrow \sigma_{pid\ = '123'}(booking) }$$
    
- Join them and project the fid:
    $$\ce{ \Pi_{ fid} (B \bowtie F) }$$

Q: Find passenger names for passengers who have bookings on at least one flight.
$$\ce{ \Pi_{pname}( passenger \bowtie  booking) }$$

**Q: Find passenger IDs (pid) who have used _all_ agencies located in 'Mumbai'.**

- Find the agency IDs in 'Mumbai':
    $$\ce{ A_{Mumbai} \leftarrow \Pi_{aid}(\sigma_{acity\ =\  'Mumbai'}(agency)) }$$
- Find all bookings by passenger and agency:
    $$\ce{ B_{PA} \leftarrow \Pi_{pid, aid}(booking) }$$
- Divide the bookings by the agencies:
    $$\ce{ Result \leftarrow B_{PA} \div A_{Mumbai} }$$

\newpage



# SQL {#sql}

\etocsettocstyle{\textbf{Chapter Contents}\par\rule{\linewidth}{0.5pt}}{\par\rule{\linewidth}{0.5pt}}
\localtableofcontents
\noindent


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

\newpage



# Views {#views}

\etocsettocstyle{\textbf{Chapter Contents}\par\rule{\linewidth}{0.5pt}}{\par\rule{\linewidth}{0.5pt}}
\localtableofcontents
\noindent


Views are virtual tables. They do not store any data themselves but are based on the result-set of an SQL query.

We create views for several reasons:

1. **Security:** To restrict access to data. We can hide sensitive columns or rows from certain users by only granting them access to a view.
2. **Simplicity:** To hide the complexity of queries. A complex join or a query with many subqueries can be saved as a view, allowing users to query it like a simple table.
3. **Consistency:** To provide a stable interface. The base tables can be restructured, but the view can be maintained to provide a consistent schema to applications.

> [!TIP] > Analogy: The Tinted Window
> Imagine a house (Database) with many rooms (Tables).
>
> - **Table**: The actual room with all its furniture (Data).
> - **View**: A tinted window that lets you see only _specific_ parts of the room (e.g., only the sofa, not the messy bed). You can't "touch" the furniture directly through the window (in complex views), but you can see it.

![\ ](images/mermaid_4fa8d2727d630d8753e3b2d87462d2c3.png){height=11cm}

One table can have any number of views.

To create views we have the following SQL command:

```sql
CREATE VIEW <viewname> AS SELECT <columns> FROM <table_name>;
```

E.g.

```sql
CREATE VIEW V1 AS SELECT rno, sname, dept FROM STUDENT where dept = 'CSIT';

CREATE VIEW Student_Course AS
SELECT s.rno, s.sname, c.cid, c.cname
FROM STUDENT s INNER JOIN COURSE c ON s.roll = c.roll;
```

Views' schemas (their definitions, not their data) are stored in the data dictionary.

At runtime, when a view is queried, the database executes the view's underlying SELECT statement, creates the virtual table, and then runs the query against it.

### Updating the View

```sql
CREATE OR REPLACE VIEW <viewname> AS SELECT <column> FROM <table>;
```

If view already exists, it will update it (replace its definition), if not, then it will create one.

### Dropping the View

If we want to drop the view,

```sql
DROP VIEW <viewname>;
```

This drops the view's definition only. It has no effect on the data in the underlying base tables.

If we drop the base table, then all the views connected to the table will become invalid and will be dropped as well.

### Insertion, Updation and Deletion in View

This is also known as "updatability". Whether a view is updatable (allows `INSERT`, `UPDATE`, `DELETE`) depends on its definition.

- **Simple Views:** Are generally updatable. A view is simple if it:
  - Refers to only one table.
  - Does _not_ use `GROUP BY` or aggregate functions (`COUNT()`, `SUM()`, etc.).
  - Does _not_ use `DISTINCT`.
- **Complex Views:** Are generally _not_ updatable. This includes:
  - Views with `JOIN`s (like `Student_Course` above).
  - Views with `GROUP BY` or aggregate functions.
  - Views using `UNION`, `INTERSECT`, or `MINUS`.

While performing DML operations on a view, all the constraints of the base table must be fulfilled (e.g., `PRIMARY KEY`, `UNIQUE`, `CHECK`).

**INSERT Example:**

```sql
INSERT INTO V1 (rno, sname, dept) VALUES (120, 'Alex', 'CSIT');
```

This will work. The row will be added to the `STUDENT` base table.

**DML Restrictions:**
If we try to INSERT into a view, what about the attributes not in the view?

- The base table's attributes which are not in the view will be given `NULL` value.
- If any of those attributes has a `NOT NULL` constraint (and no `DEFAULT` value), the `INSERT` operation will fail.

### WITH CHECK OPTION

This is a constraint that can be added to a view. It forces all `INSERT` and `UPDATE` operations on the view to conform to the `WHERE` clause in the view's definition.

```sql
CREATE VIEW V1 AS
SELECT rno, sname, dept FROM STUDENT
WHERE dept = 'CSIT'
WITH CHECK OPTION;
```

Now, consider these two operations:

> [!EXAMPLE] > Example
> **Operation 1: Success**
>
> ```sql
> UPDATE V1 SET sname = 'Alex B.' WHERE rno = 120;
> ```
>
> _Result:_ **Allowed**. The row still belongs to 'CSIT' after the name change.
>
> **Operation 2: Failure**
>
> ```sql
> UPDATE V1 SET dept = 'MECH' WHERE rno = 120;
> ```
>
> _Result:_ **Blocked**. Changing Dept to 'MECH' would make the row vanish from the view `V1` (since `V1` only shows 'CSIT'). `WITH CHECK OPTION` prevents this "disappearing act".

Without `WITH CHECK OPTION`, Operation 2 would succeed, and the row would silently disappear from the view.


\newpage



# Indexes {#indexes}

\etocsettocstyle{\textbf{Chapter Contents}\par\rule{\linewidth}{0.5pt}}{\par\rule{\linewidth}{0.5pt}}
\localtableofcontents
\noindent


### Sequences (Auto-number)

In oracle, we can create an auto-number field by using using sequences. A sequence is an object in Oracle that is used to generate a number sequence. This can be used when we need to create a unique number to act as a primary.

```sql
CREATE SEQUENCE sequence_name
    MINVALUE value
    MAXVALUE value
    START WITH value
    INCREMENT BY value
    CACHE value;
```

Once a sequence is created, you can access its values in SQL statements with

1. `CURRVAL` pseudo column which returns the current value of the sequence _for your session_, and,
2. `NEXTVAL` pseudo column, which increments the sequence and returns the new value.

#### Index Modifiers

`NOMAXVALUE` to denote a max value of $10^{27}$ for ascending sequence and -1 for descending sequence. Oracle uses this by default.

`CYCLE` to allow the sequence to generate value after it reaches the limit, min value for a descending sequence and max value for an ascending sequence.

When an ascending sequence reaches its max value, it generates min value.

On the other hand, when a descending sequence reaches its min value, it generates max value.

`NOCYCLE` is default.

`CACHE` specifies the no of sequence values oracle pre-allocates and holds in memory for faster access.

`ORDER` ensures that oracle will generate the sequence numbers in order of request.

This is useful if you are using Oracle in Real Application Clusters. When you are using exclusive mode, then oracle will always generate sequence numbers in order.

`NOORDER` if we do not want to ensure oracle to generate sequence numbers in order of request. This option is default.

Example,

```sql
CREATE SEQUENCE emp_id_seq
    INCREMENT BY 1
    START WITH 1001
    NOMAXVALUE
    NOCYCLE
    CACHE 20;
```

### How to Use a Sequence

You typically use `NEXTVAL` within an `INSERT` statement to populate a primary key column.

```sql
INSERT INTO employees (employee_id, first_name, last_name)
VALUES (emp_id_seq.NEXTVAL, 'Jane', 'Doe');
```

To retrieve the value you just inserted within your current session, you can use `CURRVAL`.

```sql
SELECT emp_id_seq.CURRVAL FROM DUAL;
```

### Index

When the user executes a select statement to search for a particular record, the oracle engine is first required to locate the table on the hard disk. The oracle engine reads system information and starts searching the location of the table in storage media.

Oracle engine then performs a sequential search (also called a **Full Table Scan**) to locate the record that matches the user's criteria. Indexing a table is an access strategy to sort and search records in the table, which avoids this slow sequential search.

> [!TIP] > Analogy: The Textbook Index
>
> - **No Index (Full Table Scan)**: To find "Deadlock" in a book, you read _every single page_ from start to finish. Slow!
> - **Index (Index Scan)**: You go to the back of the book, find "Deadlock" in the sorted list, and jump straight to Page 142. Fast!

![\ ](images/mermaid_dc15ef82eb1a0b32a32c0b14535c5baf.png){height=11cm}

Indexes are essential to improve the speed with which records can be located and retrieved from the table. It involves creating a **data structure (commonly a B-tree)** that is stored separately from the table.

Index consists of,

- **Index Key:** A sorted copy of the data from the indexed column(s).
  $\\$
- **ROWID:** An address pointer that identifies the exact physical location of the corresponding record in the table's data blocks.
  $\\$
- Whenever data is inserted, updated, or deleted in the original table, a related record automatically gets updated in all the index tables. This adds overhead to DML operations, which is why indexes should be used judiciously.
  $\\$
- Whenever a `SELECT` command is executed with a `WHERE` clause on an indexed column, the index table is automatically activated, and the database uses the index to find the ROWID, then directly fetches the row. This is much faster than a full table scan.

A table's **ROWID** identifies a row's physical address. The format you may see (`BBBBBB.RRRR.FFFF`) is the older _Restricted ROWID_. Modern Oracle databases use an _Extended ROWID_ which is more complex (using a Base64-encoded string) and includes the Data Object Number, allowing it to uniquely identify rows in different objects.

### Creating an Index

```sql
CREATE INDEX index_name
ON table_name(column1, column2, ...);
```

This syntax creates a **composite (or concatenated) index**. The index is built using _all_ listed columns, in that specific order (e.g., `column1`, then `column2`). This is **not a fallback**; it's used to speed up queries that filter on `column1`, or on `column1` _and_ `column2`.

```sql
CREATE UNIQUE INDEX index_name
ON table_name(column1, column2, ...);
```

This syntax creates a **unique index**. It enforces a constraint that no two rows in the table can have the same value (or combination of values) in the indexed column(s). `NULL` values are permitted (unless a `NOT NULL` constraint also exists). **Primary Key constraints automatically create a unique index.**

### Types of Indexes

| Index Type           | Best For                                  | Pros                              | Cons                                   |
| :------------------- | :---------------------------------------- | :-------------------------------- | :------------------------------------- |
| **B-Tree** (Default) | High Cardinality (IDs, Names, Dates)      | Fast lookups, good for ranges.    | Not good for low cardinality.          |
| **Bitmap**           | Low Cardinality (Gender, Status, Boolean) | Fast for `AND`/`OR` combinations. | Slow updates (Locking issues).         |
| **Function-Based**   | Expressions (e.g., `UPPER(name)`)         | Speeds up specific calculations.  | Only works for that specific function. |

- **B-Tree Index:** The default, standard index. Good for high-cardinality data (e.g., `employee_id`, `username`).
- **Bitmap Index:** Good for low-cardinality data (e.g., `gender`, `is_active`). Very fast for `OR` and `AND` queries on these columns, but slow to update (high DML overhead).
- **Function-Based Index:** An index built on the result of a function or expression (e.g., `CREATE INDEX idx_emp_name ON employees (UPPER(last_name))` to speed up case-insensitive searches).

### When _Not_ to Use an Index

- **On very small tables:** A full table scan is often faster because reading the index is an extra step.
- **On columns with very low cardinality (B-Tree):** A standard B-Tree index on a column like `gender` (M/F) is inefficient. A bitmap index is better here.
- **On tables with very frequent DML:** Heavy `INSERT`, `UPDATE`, and `DELETE` operations require constant index updates, which can slow down these operations.

### Managing Indexes

You can drop an index that is no longer needed:

```sql
DROP INDEX index_name;
```

You can see all indexes on a table by querying the data dictionary:

```sql
SELECT index_name, column_name
FROM USER_IND_COLUMNS
WHERE table_name = 'EMPLOYEES';
```


\newpage



# PLSQL {#plsql}

\etocsettocstyle{\textbf{Chapter Contents}\par\rule{\linewidth}{0.5pt}}{\par\rule{\linewidth}{0.5pt}}
\localtableofcontents
\noindent




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


\newpage



# Normalization {#normalization}

\etocsettocstyle{\textbf{Chapter Contents}\par\rule{\linewidth}{0.5pt}}{\par\rule{\linewidth}{0.5pt}}
\localtableofcontents
\noindent

Normalization is the process of organizing data to minimize redundancy and dependency.

## Functional Dependencies (FD)
An FD is a constraint between two sets of attributes in a relation.
Notation: $X \rightarrow Y$ ("X determines Y").

- **Determinant**: $X$ (Left side).
- **Dependent**: $Y$ (Right side).
- **Meaning**: For every unique value of $X$, there is exactly one corresponding value of $Y$.
  - _Analogy_: `SSN -> Name`. If you know the SSN, you know the Name.

### Types of FDs

1.  **Trivial FD**: $Y \subseteq X$ (e.g., $AB \rightarrow A$). Always true.
2.  **Non-Trivial FD**: $Y \not\subseteq X$ (e.g., $A \rightarrow B$).
3.  **Full FD**: $Y$ depends on the _entire_ $X$, not a subset.
4.  **Partial FD**: $Y$ depends on a _part_ of $X$ (e.g., $AB \rightarrow C$, but $A \rightarrow C$ is also true).
5.  **Transitive FD**: $X \rightarrow Y$ and $Y \rightarrow Z$, so $X \rightarrow Z$.

### Armstrong's Axioms (Inference Rules)

Used to derive all implied FDs.

1.  **Reflexivity**: If $Y \subseteq X$, then $X \rightarrow Y$.
2.  **Augmentation**: If $X \rightarrow Y$, then $XZ \rightarrow YZ$.
3.  **Transitivity**: If $X \rightarrow Y$ and $Y \rightarrow Z$, then $X \rightarrow Z$.

## Algorithms

### Closure of Attributes ($X^+$)

The set of all attributes that can be determined by $X$.

**Algorithm:**

1.  Start with $Result = X$.
2.  Loop through FDs ($A \rightarrow B$).
3.  If $A \subseteq Result$, add $B$ to $Result$.
4.  Repeat until no change.

> [!EXAMPLE] > $R(A, B, C, D, E)$ > $FDs: \{ A \rightarrow B, BC \rightarrow D, E \rightarrow C \}$
> Find $(AE)^+$:
>
> 1.  Start: $\{A, E\}$
> 2.  Use $A \rightarrow B$: Add $B$. Now $\{A, E, B\}$.
> 3.  Use $E \rightarrow C$: Add $C$. Now $\{A, E, B, C\}$.
> 4.  Use $BC \rightarrow D$: We have $B$ and $C$, so add $D$. Now $\{A, E, B, C, D\}$.
> 5.  Result: All attributes. So, $AE$ is a **Super Key**.

### Canonical Cover (Minimal Cover)

A simplified set of FDs that is equivalent to the original set but has no redundancy.

**Steps:**

1.  **Singleton RHS**: Split $A \rightarrow BC$ into $A \rightarrow B$ and $A \rightarrow C$.
2.  **Remove Extraneous LHS**: If $AB \rightarrow C$ and $A \rightarrow C$, then $B$ is extraneous. Remove it.
3.  **Remove Redundant FDs**: If an FD can be derived from others (Transitivity), remove it.

> [!EXAMPLE] > $F = \{ A \rightarrow B, B \rightarrow C, A \rightarrow C \}$
>
> - $A \rightarrow C$ is redundant because $A \rightarrow B \rightarrow C$.
> - Minimal Cover: $\{ A \rightarrow B, B \rightarrow C \}$.

#### Complex Example 1: Extraneous Attributes

**Given F:** $\{ AB \rightarrow C, A \rightarrow C, B \rightarrow D \}$

1.  **Singleton RHS:** Already singleton.
2.  **Extraneous LHS:**
    - Look at $AB \rightarrow C$.
    - Check if $A$ is extraneous: Compute $(B)^+$ using remaining FDs $\{ A \rightarrow C, B \rightarrow D \}$. $(B)^+ = \{B, D\}$. Does it contain $C$? No.
    - Check if $B$ is extraneous: Compute $(A)^+$ using remaining FDs $\{ A \rightarrow C, B \rightarrow D \}$. $(A)^+ = \{A, C\}$. Does it contain $C$? **Yes**.
    - So, $B$ is extraneous in $AB \rightarrow C$. Replace $AB \rightarrow C$ with $A \rightarrow C$.
    - New Set: $\{ A \rightarrow C, A \rightarrow C, B \rightarrow D \}$.
3.  **Remove Duplicates:** $\{ A \rightarrow C, B \rightarrow D \}$.

#### Complex Example 2: Full Reduction

**Given F:** $\{ A \rightarrow BC, B \rightarrow C, A \rightarrow B, AB \rightarrow C \}$

**Step 1: Singleton RHS**

- $A \rightarrow B$
- $A \rightarrow C$
- $B \rightarrow C$
- $AB \rightarrow C$

Current Set: $\{ A \rightarrow B, A \rightarrow C, B \rightarrow C, AB \rightarrow C \}$

**Step 2: Extraneous LHS**

- Check $AB \rightarrow C$.
- Is $B$ extraneous? $(A)^+$ using $\{ A \rightarrow B, A \rightarrow C, B \rightarrow C \}$. $(A)^+ = \{A, B, C\}$. Contains $C$? **Yes**.
- So $AB \rightarrow C$ becomes $A \rightarrow C$.

Current Set: $\{ A \rightarrow B, A \rightarrow C, B \rightarrow C, A \rightarrow C \}$

- Remove duplicates: $\{ A \rightarrow B, A \rightarrow C, B \rightarrow C \}$

**Step 3: Redundant FDs**

- Check $A \rightarrow C$. Can we derive $A \rightarrow C$ from $\{ A \rightarrow B, B \rightarrow C \}$?
- $(A)^+$ using $\{ A \rightarrow B, B \rightarrow C \}$ is $\{A, B, C\}$. Contains $C$? **Yes**.
- So $A \rightarrow C$ is redundant. Remove it.

**Final Minimal Cover:** $\{ A \rightarrow B, B \rightarrow C \}$

## Normal Forms

A series of steps to reduce redundancy.

### 1NF (First Normal Form)

- **Rule**: Atomic values only. No multi-valued attributes or repeating groups.
- **Fix**: Create a new row for each value.

> [!EXAMPLE] > 
> **Bad (Not 1NF):**
> 
> | Student | Courses |
> | :--- | :--- |
> | John | Math, Physics |
>
> **Good (1NF):**
> 
> | Student | Course |
> | :--- | :--- |
> | John | Math |
> | John | Physics |


### 2NF (Second Normal Form)

- **Rule**: Must be in 1NF **AND** No **Partial Dependency**.
- **Partial Dependency**: A non-prime attribute depends on _part_ of a composite Primary Key.
- _Analogy_: In a race, your "Finish Time" depends on (RaceID, RunnerID). But "RunnerName" depends ONLY on RunnerID. That's a partial dependency.
- **Fix**: Move the partial dependency to a new table.

> [!EXAMPLE] > 
> **Bad (Not 2NF):**
> Key: `(RaceID, RunnerID)`
> 
> | RaceID | RunnerID | FinishTime | RunnerName |
> | :--- | :--- | :--- | :--- |
> | 101 | 5 | 10:00 | Bolt |
>
> _Problem:_ `RunnerName` depends only on `RunnerID`, not `RaceID`.
>
> **Good (2NF):**
> Table 1: `(RaceID, RunnerID, FinishTime)`
> Table 2: `(RunnerID, RunnerName)`

### 3NF (Third Normal Form)

- **Rule**: Must be in 2NF **AND** No **Transitive Dependency**.
- **Transitive Dependency**: Non-Prime $\rightarrow$ Non-Prime.
- _Analogy_: `Student -> ZipCode -> City`. City depends on ZipCode, not directly on Student.
- **Fix**: Move `ZipCode -> City` to a separate "Locations" table.

> [!EXAMPLE] > 
> **Bad (Not 3NF):**
> Key: `StudentID`
> 
> | StudentID | ZipCode | City |
> | :--- | :--- | :--- |
> | 1 | 90210 | Beverly Hills |
>
> _Problem:_ `City` depends on `ZipCode`, which depends on `StudentID`.
>
> **Good (3NF):**
> Table 1: `(StudentID, ZipCode)`
> Table 2: `(ZipCode, City)`

### BCNF (Boyce-Codd Normal Form)

- **Rule**: For every FD $X \rightarrow Y$, $X$ must be a **Super Key**.
- **Stricter than 3NF**: Handles cases where a Prime attribute depends on a Non-Prime attribute.

> [!EXAMPLE] > 
> **Bad (3NF but not BCNF):**
> Table: `(Student, Course, Professor)`
> Key: `(Student, Course)`
> FDs:
>
> 1. `(Student, Course) -> Professor` (OK)
> 2. `Professor -> Course` (Problem: Professor is not a Super Key)
>
> **Good (BCNF):**
> Decompose into:
> Table 1: `(Professor, Course)`
> Table 2: `(Student, Professor)`

### 4NF (Fourth Normal Form)

- **Rule**: No **Multi-valued Dependencies (MVD)**.
- **MVD ($X \twoheadrightarrow Y$)**: $X$ determines a _set_ of values for $Y$, independent of other attributes.
- _Example_: A `Course` has multiple `Books` and multiple `Lecturers`. These are independent. Storing them in one table causes Cartesian product redundancy.

> [!EXAMPLE] > 
> **Bad (Not 4NF):**
> 
> | Course | Book | Lecturer |
> | :--- | :--- | :--- |
> | Math | Algebra | Prof. A |
> | Math | Geometry | Prof. A |
> | Math | Algebra | Prof. B |
> | Math | Geometry | Prof. B |
>
> _Problem:_ Every time you add a Lecturer, you must repeat all Books for that Course.
>
> **Good (4NF):**
> Table 1: `(Course, Book)`
> Table 2: `(Course, Lecturer)`

### 5NF (Project-Join Normal Form)

- **Rule**: No **Join Dependency**.
- **Concept**: A table that can only be losslessly decomposed into 3 or more tables (not 2). Very rare.

> [!EXAMPLE] > **Scenario:**
> Three entities: `Supplier`, `Product`, `Consumer`.
> Rule: A Supplier sells a Product to a Consumer ONLY IF:
>
> 1. Supplier sells that Product.
> 2. Consumer buys that Product.
> 3. Supplier deals with that Consumer.
>
> If you store `(Supplier, Product, Consumer)` in one table, you might have redundancy that 4NF can't catch. You must split it into three tables: `(Supplier, Product)`, `(Product, Consumer)`, `(Supplier, Consumer)`.

## Decomposition Properties

### Lossless Join

When decomposing $R$ into $R_1$ and $R_2$, the join $R_1 \bowtie R_2$ must yield exactly $R$ (no spurious tuples).

- **Condition**: $R_1 \cap R_2$ (common attributes) must be a **Key** for either $R_1$ or $R_2$.

### Dependency Preservation

All original FDs should be enforceable within the individual decomposed tables without joining.

- **Note**: BCNF is always Lossless, but **not always** Dependency Preserving. 3NF is always both.


\newpage



# Transactions {#transactions}

\etocsettocstyle{\textbf{Chapter Contents}\par\rule{\linewidth}{0.5pt}}{\par\rule{\linewidth}{0.5pt}}
\localtableofcontents
\noindent




A **Transaction** is a single logical unit of work (a sequence of operations) that accesses and possibly modifies the database.

## ACID Properties

To ensure data integrity, every transaction must satisfy:

| Property        | Description                                                                                | Responsibility                             |
| :-------------- | :----------------------------------------------------------------------------------------- | :----------------------------------------- |
| **A**tomicity   | **"All or Nothing"**. Either all operations execute, or none do.                           | **Transaction Manager** (Undo Logs)        |
| **C**onsistency | Database must move from one valid state to another (Constraints preserved).                | **Programmer** & **Integrity Constraints** |
| **I**solation   | Concurrent transactions should not interfere. T1 should not see T2's intermediate updates. | **Concurrency Control Manager** (Locks)    |
| **D**urability  | Committed changes are permanent, even after a crash.                                       | **Recovery Manager** (Redo Logs)           |

### Transaction States

1.  **Active**: Executing.
2.  **Partially Committed**: Last statement executed.
3.  **Committed**: Successfully saved.
4.  **Failed**: Error occurred.
5.  **Aborted**: Rolled back.

![\ ](images/mermaid_e90299367a579276801ab63f91cd4362.png){height=11cm}

## Schedules & Serializability

A **Schedule** is the execution order of instructions from multiple transactions.

### Serial vs. Concurrent

- **Serial Schedule**: T1 finishes, then T2 starts. (Slow, Consistent).
- **Concurrent Schedule**: T1 and T2 interleaved. (Fast, Potential Inconsistency).

> [!EXAMPLE] >
> **Serial Schedule (T1 then T2)**
>
> | Time | Transaction T1 | Transaction T2 |
> | :--- | :------------- | :------------- |
> | 1    | Read(A)        |                |
> | 2    | Write(A)       |                |
> | 3    | Commit         |                |
> | 4    |                | Read(A)        |
> | 5    |                | Write(A)       |
> | 6    |                | Commit         |
>
> **Concurrent Schedule (Interleaved)**
>
> | Time | Transaction T1 | Transaction T2 |
> | :--- | :------------- | :------------- |
> | 1    | Read(A)        |                |
> | 2    | Write(A)       |                |
> | 3    |                | Read(A)        |
> | 4    |                | Write(A)       |
> | 5    | Commit         |                |
> | 6    |                | Commit         |

### Conflict Serializability

A schedule is **Conflict Serializable** if it is equivalent to a Serial Schedule.

- **Conflict**: Two operations conflict if they are from different transactions, access the same item, and at least one is a **WRITE**.
  - $R(X), W(X)$ $\rightarrow$ Conflict.
  - $W(X), W(X)$ $\rightarrow$ Conflict.
- **Precedence Graph Algorithm:**
  1.  Nodes: Transactions.
  2.  Edge $T_i \rightarrow T_j$: If $T_i$ executes a conflicting operation _before_ $T_j$.
  3.  **Result**: If Graph has a **Cycle** $\rightarrow$ NOT Serializable. No Cycle $\rightarrow$ Serializable.

> [!EXAMPLE] > **Schedule S:** > $R_1(A), R_2(A), W_1(A), W_2(A)$
>
> **Conflicts:**
>
> 1. $R_2(A)$ vs $W_1(A)$ (No, R2 is before W1? No, in schedule order: R1, R2, W1, W2. $R_2$ is before $W_1$? Yes. $R_2 \rightarrow W_1$? No, $W_1$ is after $R_2$. Wait. $R_2$ executes, then $W_1$. Conflict is $R_2 \rightarrow W_1$. Edge $T_2 \rightarrow T_1$.)
> 2. $W_1(A)$ vs $W_2(A)$ (W1 is before W2. Edge $T_1 \rightarrow T_2$.)
>
> **Graph:** $T_2 \rightarrow T_1$ and $T_1 \rightarrow T_2$.
> **Result:** Cycle exists ($T_1 \leftrightarrow T_2$). **NOT Conflict Serializable.**

### View Serializability

Less strict than Conflict Serializability. Handles **Blind Writes** (Write without Read).

- Two schedules are **View Equivalent** if:
  1.  **Initial Read**: Same transaction reads the initial value.
  2.  **Read-From**: If $T_j$ reads value written by $T_i$ in $S_1$, it must do so in $S_2$.
  3.  **Final Write**: Same transaction performs the final write.

> [!EXAMPLE] > **Schedule S (Blind Write):** > $T_1: R(A), W(A)$ > $T_2: W(A)$ > $T_3: W(A)$
> Order: $R_1(A), W_2(A), W_1(A), W_3(A)$.
>
> **View Equivalence Check (vs Serial $T_1, T_2, T_3$):**
>
> 1.  **Initial Read:** $T_1$ reads initial A in both. (Pass)
> 2.  **Read-From:** No transaction reads from another. (Pass)
> 3.  **Final Write:** $T_3$ writes the final A in both. (Pass)
>
> **Result:** S is **View Serializable** (equivalent to $T_1 \rightarrow T_2 \rightarrow T_3$).
> _Note:_ This schedule is also Conflict Serializable ($T_2 \rightarrow T_1 \rightarrow T_3$), but View Serializability is often used to justify schedules with blind writes that might fail stricter conflict checks in more complex scenarios.

## Recoverability of Schedules

Even if a schedule is Serializable, it might not be **Recoverable**. If a transaction fails, we must ensure we can rollback without affecting committed transactions.

### Recoverable Schedule

A schedule is **Recoverable** if for every pair of transactions $T_i$ and $T_j$ such that $T_j$ reads a value written by $T_i$, $T_i$ must **commit before** $T_j$ commits.

- **Rule:** If $T_2$ reads from $T_1$, then $C_1 < C_2$.
- **Why?** If $T_2$ commits first and then $T_1$ aborts, $T_2$ has read invalid data but cannot be rolled back (Durability property). This is an unrecoverable state.

> [!EXAMPLE] > Unrecoverable vs Recoverable
>
> - **Unrecoverable:** $W_1(A), R_2(A), C_2, C_1$ (If T1 fails, T2 is already committed with dirty data).
> - **Recoverable:** $W_1(A), R_2(A), C_1, C_2$ (If T1 fails, T2 can still be aborted).

### Cascadeless Schedule (ACA - Avoid Cascading Aborts)

A schedule is **Cascadeless** if it avoids the "Domino Effect" of rollbacks.

- **Rule:** $T_j$ can only read data written by $T_i$ **after** $T_i$ has committed.
- **Benefit:** No cascading rollbacks. If $T_1$ fails, no other transaction needs to be rolled back because no one read its dirty data.

> [!EXAMPLE] > Cascading vs Cascadeless
>
> - **Cascading:** $W_1(A), R_2(A), R_3(A), Abort_1$ (T2 and T3 must also abort).
> - **Cascadeless:** $W_1(A), C_1, R_2(A), C_2$ (T2 reads only committed data).

### Strict Schedule

The most restrictive and practical level.

- **Rule:** A transaction can neither **Read nor Write** a data item $X$ until the last transaction that wrote $X$ has committed (or aborted).
- **Benefit:** Simplifies recovery (Undo involves simply restoring the "Before Image").

### Hierarchy
> Strict $\subset$ Cascadeless $\subset$ Recoverable $\subset$ All Schedules


\newpage



# Concurrency {#concurrency}

\etocsettocstyle{\textbf{Chapter Contents}\par\rule{\linewidth}{0.5pt}}{\par\rule{\linewidth}{0.5pt}}
\localtableofcontents
\noindent

Concurrency Control is the procedure used by the Database Management System (DBMS) to allow multiple transactions to run simultaneously (concurrently) without violating the consistency of data.

If transactions are executed serially (one after another), consistency is guaranteed, but system throughput (efficiency) is very low. Concurrency improves throughput but introduces several problems.

### Problems due to Concurrency

| Problem                           | Description                                                                                                                                     | Example                                                                                   |
|:--------------------------------- |:----------------------------------------------------------------------------------------------------------------------------------------------- |:----------------------------------------------------------------------------------------- |
| **Lost Update**                   | Two transactions access the same data item and have their operations interleaved in a way that makes the value of some database item incorrect. | T1 and T2 update the same record; T2's write overwrites T1's write.                       |
| **Dirty Read (Temporary Update)** | A transaction reads a value written by another transaction that has not yet committed.                                                          | T2 reads a value updated by T1. T1 fails and rolls back. T2 has read invalid data.        |
| **Unrepeatable Read**             | A transaction reads the same item twice and gets different values because another transaction modified it in between.                           | T1 reads X, T2 modifies X and commits, T1 reads X again and gets a different value.       |
| **Phantom Read**                  | A transaction executes a query twice and gets a different set of rows because another transaction inserted or deleted rows.                     | T1 counts employees. T2 adds a new employee. T1 counts again and gets a different number. |

#### Lost Update Problem (Write-Write Conflict)
This occurs when two transactions update the same data item, but the second update overwrites the first update because it didn't know about it.

**Example:**
Suppose A = 100.

| Time | T1         | T2         | Value of A in DB |
|:---- |:---------- |:---------- |:---------------- |
| t1   | Read(A)    |            | 100              |
| t2   |            | Read(A)    | 100              |
| t3   | A = A - 50 |            | 100              |
| t4   |            | A = A + 20 | 100              |
| t5   | Write(A)   |            | **50**           |
| t6   |            | Write(A)   | **120**          |

**Result:** The update from T1 (subtracting 50) is completely lost. The final value should be 70, but it is 120.

#### Dirty Read Problem (Write-Read Conflict)
This occurs when a transaction reads data that has been updated by another transaction that has *not yet committed*. If the other transaction rolls back, the first transaction has read data that technically never existed.

**Example:**

| Time | T1           | T2      |
|:---- |:------------ |:------- |
| t1   | Read(A)      |         |
| t2   | A = A + 100  |         |
| t3   | Write(A)     |         |
| t4   |              | Read(A) |
| t5   | ...Error...  |         |
| t6   | **Rollback** |         |

**Result:** T2 has read the updated value of A. But T1 failed and rolled back A to its original value. T2 is now working with "dirty" (incorrect) data.

#### Unrepeatable Read Problem (Read-Write Conflict)
This occurs when a transaction reads the same variable twice during its execution. Between the two reads, another transaction updates the value.

**Example:**

| Time | T1      | T2          |
|:---- |:------- |:----------- |
| t1   | Read(A) |             |
| t2   |         | Read(A)     |
| t3   |         | A = A + 100 |
| t4   |         | Write(A)    |
| t5   | Read(A) |             |

**Result:** T1 reads A at t1 (say 100) and at t5 (say 200). The data has changed unexpectedly during the transaction.

## 
## Deadlock Handling in Concurrency
Deadlocks occur when two or more transactions are waiting indefinitely for one another to release locks.

**Example:**
```sql
T1: Lock(A) ... waiting for B ...
T2: Lock(B) ... waiting for A ...
```

### Necessary Conditions (Coffman Conditions)

Deadlock can occur only if **ALL** four conditions hold simultaneously:

1.  **Mutual Exclusion**: At least one resource is non-sharable (only one transaction can use it at a time).
2.  **Hold and Wait**: A transaction holding at least one resource is waiting to acquire additional resources held by others.
3.  **No Preemption**: Resources cannot be forcibly taken from a transaction; they must be released voluntarily.
4.  **Circular Wait**: A set of transactions $\{T_0, T_1, ..., T_n\}$ exists such that $T_0$ waits for $T_1$, $T_1$ waits for $T_2$, ..., and $T_n$ waits for $T_0$.

### Handling Deadlocks

#### Deadlock Prevention
We ensure that one of the necessary conditions for deadlock (Mutual Exclusion, Hold and Wait, No Preemption, Circular Wait) never holds.
- **Wait-Die Scheme:** (Based on timestamps)
    - If older T1 requests lock held by younger T2: T1 waits.
    - If younger T2 requests lock held by older T1: T2 dies (rolls back).
- **Wound-Wait Scheme:**
    - If older T1 requests lock held by younger T2: T1 wounds T2 (T2 rolls back).
    - If younger T2 requests lock held by older T1: T2 waits.

#### Deadlock Detection & Recovery

Allow deadlocks to occur, detect them, and recover.

- **Wait-For Graph**: A directed graph where nodes are transactions and edge $T_i \rightarrow T_j$ means $T_i$ is waiting for $T_j$.
- **Cycle Detection**: If the graph has a cycle, a deadlock exists.

![\ ](images/mermaid_1502401081c7041895920ff56c6e1bae.png){height=11cm}

- **Recovery**: Select a **Victim** to rollback based on:
  - Cost (least progress).
  - Number of items locked.
  - Number of rollbacks already occurred (to avoid starvation).


\newpage



# Concurrency Control {#concurrency-control}

\etocsettocstyle{\textbf{Chapter Contents}\par\rule{\linewidth}{0.5pt}}{\par\rule{\linewidth}{0.5pt}}
\localtableofcontents
\noindent

These are the rules the DBMS follows to ensure that concurrent transactions do not cause inconsistency.

### Lock-Based Protocols
A **lock** is a variable associated with a data item that describes the status of that item with respect to possible operations that can be applied to it.

**Types of Locks:**
1.  **Shared Lock (S-lock):** Also called a Read Lock. If T1 has an S-lock on item A, T1 can read A but cannot write A. Any other transaction T2 can also acquire an S-lock on A (multiple transactions can read simultaneously).
2.  **Exclusive Lock (X-lock):** Also called a Write Lock. If T1 has an X-lock on item A, T1 can both read and write A. No other transaction can acquire *any* lock (S or X) on A.

**Lock Compatibility Matrix:**

| Current Lock      | Request Shared (S) | Request Exclusive (X) |
|:----------------- |:------------------ |:--------------------- |
| **None**          | Grant              | Grant                 |
| **Shared (S)**    | Grant              | Wait                  |
| **Exclusive (X)** | Wait               | Wait                  |

#### Two-Phase Locking (2PL) Protocol
This protocol ensures serializability. It requires that each transaction issues lock and unlock requests in two phases.

1.  **Growing Phase:** A transaction may obtain locks, but may not release any lock.
2.  **Shrinking Phase:** A transaction may release locks, but may not obtain any new locks.

**Example:**
```sql
T1:
	Lock-X(A) // Growing
	Lock-S(B) // Growing
	Read(B)
	Write(A)
	Unlock(A) // Shrinking starts - Cannot acquire any more locks
	Unlock(B)
```
- **Advantage:** Guarantees conflict serializability.
- **Disadvantage:** Does *not* prevent deadlocks. Cascading rollbacks are possible (if strict 2PL is not used).

#### Strict Two-Phase Locking (Strict 2PL)
This is the most widely used variation.
- **Rule:** Same as 2PL, but a transaction must hold all its **Exclusive locks** until it commits or aborts.
- **Advantage:** Prevents cascading rollbacks. Prevents dirty reads.

#### Rigorous Two-Phase Locking (Rigorous 2PL)
- **Rule:** Same as 2PL, but a transaction must hold **ALL locks** (Shared and Exclusive) until it commits or aborts.
- **Advantage:** Easier to implement, but less concurrency than Strict 2PL.

### Timestamp-Ordering Protocols
This protocol ensures serializability by selecting an order for transactions in advance.
- **Timestamp (TS):** A unique identifier assigned to each transaction. If T1 starts before T2, then `TS(T1) < TS(T2)`.
- **Data Item Timestamps:** Every data item `Q` has two values:
    - **W-timestamp(Q):** The largest timestamp of any transaction that successfully executed `write(Q)`.
    - **R-timestamp(Q):** The largest timestamp of any transaction that successfully executed `read(Q)`.

**The Protocol Rules:**
Suppose transaction `Ti` wants to issue `read(Q)` or `write(Q)`.

1.  **Ti issues Read(Q):**
    - If `TS(Ti) < W-timestamp(Q)`: `Ti` needs a value that was already overwritten by a younger transaction. **Reject** `Ti` and rollback.
    - Otherwise: Execute `read(Q)` and update `R-timestamp(Q) = max(R-timestamp(Q), TS(Ti))`.

2.  **Ti issues Write(Q):**
    - If `TS(Ti) < R-timestamp(Q)`: A younger transaction has already read the value `Ti` wants to update. **Reject** and rollback (to prevent invalidating the read).
    - If `TS(Ti) < W-timestamp(Q)`: A younger transaction has already written a new value. **Reject** and rollback (Thomas' Write Rule is an exception here).
    - Otherwise: Execute `write(Q)` and update `W-timestamp(Q) = TS(Ti)`.

- **Advantages:** Guarantees serializability; Ensures freedom from deadlock.
- **Disadvantages:** High overhead; Possibility of starvation (long transactions might keep getting restarted).

### Validation-Based Protocols (Optimistic Concurrency Control)
This protocol assumes conflicts are rare. It allows transactions to execute without locking, and checks for conflicts only at the end.

**Three Phases:**
1.  **Read Phase:** Transaction executes and reads data into local variables. It performs writes on temporary local variables, not the database.
2.  **Validation Phase:** The transaction checks if committing its changes would violate serializability (checks for overlaps with other active transactions).
3.  **Write Phase:** If validation succeeds, the updates are applied to the database. If it fails, the transaction is rolled back.


\newpage



# Recovery {#recovery}

\etocsettocstyle{\textbf{Chapter Contents}\par\rule{\linewidth}{0.5pt}}{\par\rule{\linewidth}{0.5pt}}
\localtableofcontents
\noindent


Recovery ensures **Atomicity** and **Durability** by restoring the database to a consistent state after a failure.

## Failure Classification

1.  **Transaction Failure**: Logical error (Divide by Zero) or System error (Deadlock).
2.  **System Crash**: Hardware/Software freeze. Volatile memory (RAM) lost.
3.  **Disk Failure**: Head crash. Non-volatile storage lost. Requires backups.

## Log-Based Recovery

The system maintains a **Log** (Journal) on stable storage recording all updates.
**Write-Ahead Logging (WAL)**:

1.  Log record must be written to stable storage _before_ the database item is updated on disk.
2.  Log must be saved _before_ commit.

### Deferred Database Modification

No updates are made to the database on disk until the transaction **Commits.**

- **During Execution:** All writes are kept in buffers/logs.
- **Recovery:**
  - **Crash before Commit:** Ignore transaction (Nothing was written to disk).
  - **Crash after Commit:** **Redo** the updates from the log.
  - **Undo** is NEVER needed.

> [!EXAMPLE] > Deferred Modification
>
> - **Log:** `[Start T1]`, `[Write T1, A, 100]`, `[Commit T1]`, `[Crash]`
> - **Recovery:** Since T1 committed, the system **Redoes** `[Write T1, A, 100]` to ensure A=100 is on disk.
> - If crash happened _before_ `[Commit T1]`, the system would simply **Ignore** T1.

### Immediate Database Modification

Updates can be written to the database on disk **any time** (even before commit).

- **Recovery:**
  - **Crash before Commit:** **Undo** the changes (Restore old values).
  - **Crash after Commit:** **Redo** the changes (Ensure new values are persisted).

> [!EXAMPLE] > Immediate Modification
>
> - **Log:** `[Start T1]`, `[Write T1, A, 50, 100]`, `[Crash]` (No Commit)
> - **Recovery**: T1 was active but didn't commit. The system **Undoes** the write, restoring A to 50.
> - If `[Commit T1]` was present, the system would **Redo** to ensure A=100.

## Checkpoints

To avoid replaying the _entire_ log during recovery, **Checkpoints** are used.

**Process:**

1.  Output all log records to disk.
2.  Output all dirty database pages to disk.
3.  Write `<CHECKPOINT>` to log.

**Recovery Algorithm:**

1.  Scan backwards to find the last `<CHECKPOINT>`.
2.  Transactions committed _before_ checkpoint: **Ignore** (Already saved).
3.  Transactions active _during/after_ checkpoint: **Redo** or **Undo** based on status.

## Shadow Paging

A non-log-based technique.

Maintain two Page Tables: **Current** and **Shadow.**

- **Operation:**
  - **Read**: Use Current Page Table.
  - **Write**: Copy page to a new block, modify it, and update Current Page Table to point to new block. Shadow Page Table still points to old block.
  - **Commit**: Atomically switch Shadow Page Table to point to Current Page Table.
- **Cons**: Data fragmentation. Garbage collection overhead.

> [!TIP] > Analogy: Shadow Paging
> Think of editing a document:
>
> - **Current Page Table:** The "Draft" you are working on.
> - **Shadow Page Table:** The "Saved" version on disk.
> - **Commit**: You hit "Save As" and overwrite the old file with the new one. If the power goes out _before_ you save, you just open the old file (Shadow) and nothing is corrupted.

![\ ](images/mermaid_f54d9468e366dd56870d8c280a4ed51e.png){height=11cm}

## ARIES Algorithm

**Algorithms for Recovery and Isolation Exploiting Semantics.** The industry standard (used by IBM DB2, SQL Server).

**Phases:**
1.  **Analysis:** Scan log forward from last checkpoint to identify "Dirty Pages" and "Active Transactions".
2.  **Redo:** Replay _all_ updates (even for failed transactions) to bring DB to the state at the moment of crash. ("Repeating History").
3.  **Undo:** Scan log backward to rollback uncommitted transactions.

> [!EXAMPLE] > ARIES Recovery Scenario
>
> - **Log**: `[Start T1]`, `[Write T1, A, 10, 20]`, `[Start T2]`, `[Write T2, B, 5, 15]`, `[Commit T1]`, `[Crash]`
>
> **1. Analysis Phase:**
>
> - Determines that at the time of crash, **T2 was active** and **T1 was committed**.
> - Identifies Dirty Pages (A and B might be in memory but not disk).
>
> **2. Redo Phase *(Repeating History)*:**
>
> - Reapplies `[Write T1, A]` and `[Write T2, B]`.
> - Now the database state matches exactly what was in memory before the crash.
>
> **3. Undo Phase:**
>
> - Since **T2** was active (not committed), it must be rolled back.
> - Undoes `[Write T2, B]` (Restores B to 5).
> - Writes `[Abort T2]` to log.


\newpage



# Microsoft Azure SQL {#microsoft-azure-sql}

\etocsettocstyle{\textbf{Chapter Contents}\par\rule{\linewidth}{0.5pt}}{\par\rule{\linewidth}{0.5pt}}
\localtableofcontents
\noindent

#case_study

**Azure SQL Database** is a fully managed Platform as a Service (PaaS) database engine that handles most of the database management functions such as upgrading, patching, backups, and monitoring without user involvement.

## Architecture (Control Plane vs Data Plane)

Azure SQL separates the management layer from the data layer to ensure high availability and scalability.

- **Control Plane**: Manages deployment, health monitoring, failover, and billing. It acts as the "Brain".
- **Data Plane**: Handles the actual user queries and data storage. It consists of the SQL Server engine nodes.

## Deployment Models

Choose the right level of isolation and resource sharing.

| Model                | Description                                                                                      | Best For                                                               |
| :------------------- | :----------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------- |
| **Single Database**  | A fully isolated database with its own set of resources (CPU, Memory).                           | New apps, microservices, predictable workloads.                        |
| **Elastic Pool**     | A collection of databases sharing a _pool_ of resources. Cost-effective for unpredictable usage. | SaaS apps with many tenants (e.g., 1000 databases with low avg usage). |
| **Managed Instance** | A nearly 100% compatible SQL Server instance. Supports cross-database queries, SQL Agent, CLR.   | Lift-and-shift migrations from on-premise SQL Server.                  |

## Purchasing Models & Service Tiers

### Purchasing Models

1.  **DTU (Database Transaction Unit):** A bundled measure of CPU, Memory, and IO. Simple, pre-configured performance.
2.  **vCore (Virtual Core):** Independent scaling of Compute and Storage. More flexibility and control (like choosing your own server specs).

### Service Tiers

| Tier                  | Description                                                           | Storage                          | HA/DR                    |
| :-------------------- | :-------------------------------------------------------------------- | :------------------------------- | :----------------------- |
| **General Purpose**   | Budget-friendly. Separates compute from storage (Azure Blob Storage). | Remote Storage (Higher Latency)  | 1 Replica                |
| **Business Critical** | High performance. Local SSD storage attached to the compute node.     | Local SSD (Low Latency)          | 3 Replicas + 1 Read-Only |
| **Hyperscale**        | Limitless scale. Storage grows automatically up to 100TB.             | Distributed Storage Architecture | Rapid Scale-out          |

## High Availability & Disaster Recovery

Azure SQL guarantees 99.99% to 99.995% availability.

- **Active Geo-Replication:** Creates readable secondary databases in different Azure regions. If the primary region fails, you can failover to a secondary.
- **Auto-Failover Groups:** Automatically manages replication and failover of a group of databases to another region.
- **Point-in-Time Restore (PITR):** Restore the database to _any second_ in the past (up to 35 days) to recover from accidental data deletion.

## Security Features (The "Defense in Depth" Strategy)

1.  **Network Security:**
    - **Firewall Rules:** Allow traffic only from specific IPs.
    - **VNET Integration:** Private connection within Azure.
2.  **Access Management:**
    - **Azure Active Directory (AAD):** Centralized identity management (MFA, SSO).
3.  **Data Protection:**
    - **TDE (Transparent Data Encryption):** Encrypts data _at rest_ (on disk).
    - **TLS:** Encrypts data _in transit_.
    - **Always Encrypted:** Encrypts sensitive data (like credit cards) _in use_ (client-side encryption). The DB engine never sees the plaintext.
4.  **Advanced Threat Protection:**
    - Detects SQL Injection, anomalous login attempts, and potential vulnerabilities.

## Intelligent Features

- **Automatic Tuning:** The AI analyzes your queries and automatically:
  - Creates missing indexes.
  - Drops unused indexes.
  - Fixes query plan regressions.
- **Intelligent Query Processing:** Optimizes query execution plans based on runtime data.

## Comparison: Azure SQL vs SQL Server (On-Premises)

| Feature           | Azure SQL (PaaS)                                 | SQL Server (On-Premises)                     |
| :---------------- | :----------------------------------------------- | :--------------------------------------- |
| **Management**    | Fully Managed (Auto-patching, Backups)           | Manual (You manage OS, patches, backups) |
| **CapEx vs OpEx** | OpEx (Pay-as-you-go)                             | CapEx (Buy hardware/licenses upfront)    |
| **Version**       | Always the latest stable version ("Versionless") | Specific versions (2019, 2022)           |
| **OS Access**     | No OS access                                     | Full OS control                          |


\newpage



# Joins {#joins}

\etocsettocstyle{\textbf{Chapter Contents}\par\rule{\linewidth}{0.5pt}}{\par\rule{\linewidth}{0.5pt}}
\localtableofcontents
\noindent


Combines rows from two or more tables based on a related column.

We need to join tables when we do not have the desired data in one table.

| Join Type      | Description                                                                  | Venn Diagram Analogy      |
| :------------- | :--------------------------------------------------------------------------- | :------------------------ |
| **INNER JOIN** | Returns records that have matching values in **both** tables.                | Intersection ($A \cap B$) |
| **LEFT JOIN**  | Returns all records from the left table, and matched records from the right. | $A$ (entire circle)       |
| **RIGHT JOIN** | Returns all records from the right table, and matched records from the left. | $B$ (entire circle)       |
| **FULL JOIN**  | Returns all records when there is a match in either left or right table.     | Union ($A \cup B$)        |

```sql
SELECT S.Name, C.CourseName
FROM Student S
INNER JOIN Enrollments E ON S.ID = E.StudentID
INNER JOIN Courses C ON E.CourseID = C.ID;
```

#### Inner Join

Fetches common tuples (rows that have matching values in both tables).

```sql
SELECT supplier.supplier_id, supplier.supplier_name, orders.order_date 
FROM supplier INNER JOIN orders
ON supplier.supplier_id = orders.supplier_id;
```

#### Outer Join

Fetches all tuples from one table and the common ones from the other.

- **Left Outer Join:** All tuples from A (the "left" table) and the common ones from B.
- **Right Outer Join:** All tuples from B (the "right" table) and the common ones from A.
- **Full Outer Join:** All tuples from both tables.

```sql
SELECT supplier.supplier_id, supplier.supplier_name, orders.order_date 
FROM supplier RIGHT JOIN orders
ON supplier.supplier_id = orders.supplier_id;
```

```sql
SELECT supplier.supplier_id, supplier.supplier_name, orders.order_date 
FROM supplier FULL JOIN orders
ON supplier.supplier_id = orders.supplier_id;
```

#### Equi Join

This is a join that only uses an equality operator (=) in its condition.

The "Inner Join" example above is an Equi Join. The older ANSI-89 syntax also performs an Equi Join:

```sql
SELECT columns 
FROM table1, table2, table3 .... 
WHERE table1.column_name = table2.column_name; 
```

It is better practice to use the `INNER JOIN...ON` syntax to separate the join logic from the `WHERE` clause filtering logic.

#### Self Join

When one table is joined with itself. We _must_ use table aliases (like `a` and `b`) to distinguish the two instances of the table.

```sql
-- Find employees who earn less than other employees
SELECT a.name, a.salary, b.name, b.salary
FROM Customers a, Customers b
WHERE a.salary < b.salary;
```

\newpage

