Links: [[10 Concurrency]]
___
# Concurrency Control Protocols
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
