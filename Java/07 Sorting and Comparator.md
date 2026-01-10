Links: [[06 Collections]]
___
# Sorting and Comparator

The Java sort methods use **Timm sort**, which is a hybrid of insertion sort and merge sort.

We use the following to sort a collection:

```java
Arrays.sort();
Collections.sort();
```

`Arrays.sort()` can sort static arrays like `int []`

`Collections.sort()` sorts lists (like `ArrayList`).

### Comparable Interface

It is used to sort the data or object in its **natural order**, inside the class itself.

It provides one method to implement: `compareTo(T o)`.

We implement the `Comparable` interface in the class whose objects are to be arranged.

`compareTo(T o)` compares this object with the other object o.

- **Negative int:** `this` object comes _before_ `o`.
- **Positive int:** `this` object comes _after_ `s2`.
- **Zero:** `this` object and `o` are equal in terms of sorting.

```java
// Student class now defines its "natural order" as sorting by roll number
class Student implements Comparable<Student>{
    int roll;
    String name;

    // Constructor...

    @Override
    public int compareTo(Student other) {
        // We want to sort by roll number
        // 'this' is the first object, 'other' is the second
        return this.roll - other.roll;
    }
}

// Now you can just call:
Collections.sort(listOfStudents);
```

### Comparator Interface

This is used when we want to define a custom sorting order, _separate_ from the class.

Use a `Comparator` when:

- You want to sort in an order _other_ than the natural order.
- You want to sort objects of a class you _cannot modify_.
- You want to define _multiple different ways_ to sort (e.g., by name, by roll, by grade).

It provides one main method: `compare(T o1, T o2)`.

It is implemented in a separate class.

```java
// A separate class to define sorting by name
class SortStudentByName implements Comparator<Student> {

    @Override
    public int compare(Student s1, Student s2) {
        // Use String's built-in compareTo for alphabetical sorting
        return s1.name.compareTo(s2.name);
    }
}

// Now you can sort using this new logic:
Collections.sort(listOfStudents, new SortStudentByName());
```

### Sorting with Lambda Expressions

Since `Comparator` is a **[[10 Functional Interface]]** (it has only one abstract method), we can use a lambda expression instead of writing a whole new class.

```java
// Sort by name using a lambda
Comparator<Student> byName = (s1, s2) -> s1.name.compareTo(s2.name);

// Sort by roll using a lambda
Comparator<Student> byRoll = (s1, s2) -> s1.roll - s2.roll;

// You can pass the lambda directly into the sort method:
Collections.sort(listOfStudents, (s1, s2) -> s1.name.compareTo(s2.name));

// We can even "chain" comparators
// Sort by name, and if names are the same, sort by roll
Comparator<Student> byNameThenRoll = ExampleStudent.byName
        .thenComparing(ExampleStudent.byRoll);
Collections.sort(listOfStudents, byNameThenRoll);
```
