Links: 
___
# Relational Algebra

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
$$ \ce{\sigma_{ subject = 'database' \ and \ price = 1000} (Books)} $$
$$ \ce{\sigma_{branch\_name ='Perryride'}(Loan)} $$
$$ \ce{\sigma_{Amount > 1000\  \wedge\ Branch\_name \neq 'Perryride'}(Loan)} $$

#### Project ($\Pi$)

Selects a subset of attributes (columns) from a relation. It automatically removes duplicate rows from the result, as relations are sets.

$$\Pi_{A1, A2, A3}(r)$$
where,
$A_{i}$ are attribute names and
$r$ is relation
E.g. To get only the name and duration from the Course table:
$$ \ce{\Pi_{Name, Duration}(Course)} $$

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

1. $\ce{AllStudentsAndCourses(StudentID, CourseID)}$
    
2. $\ce{CS\_Courses(CourseID) = \Pi_{CourseID}(\sigma_{Dept\ =  \ 'CS'}(Course))}$
    
3. $\ce{Result(StudentID) = AllStudentsAndCourses \div CS\_Courses}$

### Queries in Relational Algebra

Given the following schema:
```
passenger(pid, pname, pgender, pcity)
agency(aid, aname, acity)
flight(fid, fdate, time, src, dest)
booking(pid, aid, fid, fdate)
```

Q: Find all flights to 'New Delhi'.
$$\ce{\sigma_{dest\ =\ 'New Delhi'} (flight)}$$

Q: Find all flights from 'Chennai' to 'New Delhi'.
$$ \ce{\sigma_{src\ =\ 'Chennai'\ and\ dest\ =\ 'New Delhi'} (flight)} $$

**Q: Find only the flight numbers (fid) for passenger with pid '123' for flights to 'Chennai' before '06.11.2020'.**
- First, find the relevant flights:
    $$ \ce{F \leftarrow \sigma_{ dest\ =\  'Chennai'\ and\ fdate\ <\ '06.11.2020'}(flight)} $$
    
- Next, find the relevant bookings:
    $$ \ce{B \leftarrow \sigma_{pid\ = '123'}(booking)} $$
    
- Join them and project the fid:
    $$ \ce{\Pi_{ fid} (B \bowtie F)} $$

Q: Find passenger names for passengers who have bookings on at least one flight.
$$ \ce{\Pi_{pname}( passenger \bowtie  booking)} $$

**Q: Find passenger IDs (pid) who have used _all_ agencies located in 'Mumbai'.**

- Find the agency IDs in 'Mumbai':
    $$ \ce{A_{Mumbai} \leftarrow \Pi_{aid}(\sigma_{acity\ =\  'Mumbai'}(agency))} $$
- Find all bookings by passenger and agency:
    $$ \ce{B_{PA} \leftarrow \Pi_{pid, aid}(booking)} $$
- Divide the bookings by the agencies:
    $$ \ce{Result \leftarrow B_{PA} \div A_{Mumbai}} $$