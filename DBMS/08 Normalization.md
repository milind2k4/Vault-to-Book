Links: [[02 Relational Data Model]]
___
# Database Design & Normalization
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
