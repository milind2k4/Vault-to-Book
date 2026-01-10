Links: [[00 DBMS]]
___
# Entity-Relationship (ER) Model

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
