
Links: [[College/Operating System/08 Concurrency]]
___
# Synchronization

It is a mechanism to control access of multiple threads to shared resources.

If we don't do synchronization, it leads to:

- **Race condition:** A situation where the outcome of an operation depends on the unpredictable sequence or timing of other threads' operations.
- **Data inconsistency:** The shared data is left in an incorrect or invalid state.
We can achieve synchronization using several mechanisms:

### Mutual Exclusion (Mutex)

A **Mutex** (or lock) is a simple synchronization primitive. It ensures that only one thread can be in a **critical section** (the part of the code accessing the shared resource) at a time.

- A thread **acquires** the lock before entering the critical section.
- If the lock is already held, the thread blocks (waits) until the lock is **released**.
- The thread **releases** the lock after exiting the critical section.

### Semaphores

A semaphore is a more general synchronization tool. It manages a counter (a number of "permits").

- **Counting Semaphore:** Allows up to $N$ threads to access a resource. A thread must `acquire()` a permit to proceed. If the counter is zero, the thread blocks. When done, it `release()` the permit.
- **Binary Semaphore:** A semaphore with $N=1$. It acts just like a Mutex.

### Monitors (Java's `synchronized`)

A **Monitor** is a high-level construct that combines a Mutex with condition variables, making synchronization easier. Java's `synchronized` keyword is a built-in implementation of a monitor.

- **Synchronized Method:**    
    ```java
    public synchronized void safeMethod() {
        // This entire method is a critical section.
        // The lock is on the 'this' object instance.
    }
    ```
    
- **Synchronized Block:**
    ```java
    public void myMethod() {
        // ... non-critical code ...
    
        // The lock can be 'this' or any other shared object
        synchronized(this) { 
            // Critical section: only one thread at a time
            // can execute this block on the *same object*.
        }
    
        // ... other non-critical code ...
    }
    ```
    
- **Static Synchronized Method:**
    ```java
    public static synchronized void safeStaticMethod() {
        // The lock is on the Class object (e.g., MyClass.class),
        // not an instance.
    }
    ```

### Key Thread Methods

- **`sleep(long millis)`**: (Static method) Pauses the **current** thread for a specified time. **It does not release any locks it holds.**
- **`join()`**: A thread (`t1`) calls `t2.join()`. This makes `t1` (the _calling_ thread) wait until `t2` (the thread the method is called on) completes its execution. Join kills the thread it is used on. 
- **`yield()`**: (Static method) A hint to the thread scheduler that the current thread is willing to give up its current time slice. The scheduler may ignore this. It transfers thread from running to runnable. It does not kill the thread. 
- **`isAlive()`**: Checks if a thread has been started and has not yet died.
- **`wait()`, `notify()`, `notifyAll()`**: These are methods of the `Object` class (not `Thread`) and are used for inter-thread communication, typically within `synchronized` blocks.
    - **`wait()`**: Causes the current thread to release the lock and wait.
    - **`notify()`**: Wakes up a single waiting thread.
    - **`notifyAll()`**: Wakes up all waiting threads.

