Links: [[01 Entity Relation Diagram]], [[03 Relational Algebra]]
___
# Relational Data Model

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
