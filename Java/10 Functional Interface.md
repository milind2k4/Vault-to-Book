Links: [[09 Synchronization]]

---

# Functional Interface

A **Functional Interface** is an interface that contains exactly one abstract method. It can have any number of default or static methods.

It is also known as **SAM** (Single Abstract Method) interface.

The `Runnable` interface is a classic example: it has only one abstract method `void run()`.

We use the `@FunctionalInterface` annotation to ensure compile-time checking.

## Functional Programming in Java

Java 8 introduced functional programming features, allowing for more concise and declarative code.

### Key Concepts

1.  **Pure Functions**: Functions that always produce the same output for the same input and have no side effects.
2.  **Immutability**: Data objects are not modified after creation.
3.  **Higher-Order Functions**: Functions that can take other functions as arguments or return them as results.

### Example: Returning a Function

```java
// Higher-Order Function Example
public Function<Integer, Integer> createMultiplier(int factor) {
    // Returns a function that multiplies by 'factor'
    return (n) -> n * factor;
}

Function<Integer, Integer> doubler = createMultiplier(2);
System.out.println(doubler.apply(5)); // Output: 10
```

## Lambda Expressions

Lambda expressions are a concise way to represent an anonymous function that implements a functional interface.

**Syntax**: `(parameters) -> { body }`

### Use in Threads

**Old Way (Anonymous Class):**

```java
Runnable r1 = new Runnable() {
    public void run() { System.out.println("Old"); }
};
```

**New Way (Lambda):**

```java
Runnable r2 = () -> System.out.println("New");
Thread t = new Thread(r2);
t.start();
```

## Types of Functional Interface

Java provides built-in functional interfaces in the `java.util.function` package.

### Consumer

Takes an argument and returns nothing (`void`). Used for performing actions.

- **Method**: `void accept(T t)`

```java
Consumer<String> printer = (s) -> System.out.println(s);
printer.accept("Hello Consumer");
```

### Supplier

Takes no argument and returns a value. Used for lazy generation of values.

- **Method**: `T get()`

```java
Supplier<Double> randomValue = () -> Math.random();
System.out.println(randomValue.get());
```

### Function

Takes an argument and returns a result. Used for transformation.

- **Method**: `R apply(T t)`

```java
Function<String, Integer> lengthFinder = (s) -> s.length();
System.out.println(lengthFinder.apply("Hello")); // 5
```

### Predicate

Takes an argument and returns a boolean. Used for conditional checks.

- **Method**: `boolean test(T t)`

```java
Predicate<Integer> isEven = (n) -> n % 2 == 0;
System.out.println(isEven.test(4)); // true
```

## Method References

A shorthand notation of a lambda expression to call a method.

**Syntax**: `ClassName::methodName`

```java
List<String> names = Arrays.asList("a", "b", "c");

// Lambda
names.forEach(s -> System.out.println(s));

// Method Reference
names.forEach(System.out::println);
```

## Stream API

The Stream API (`java.util.stream`) is used to process collections of objects in a functional style.

**Operations:**

- **Intermediate**: `filter`, `map`, `sorted` (Lazy)
- **Terminal**: `collect`, `forEach`, `reduce` (Eager)

```java
List<String> names = Arrays.asList("Alice", "Bob", "Charlie");

List<String> result = names.stream()
    .filter(s -> s.startsWith("A"))
    .map(String::toUpperCase)
    .collect(Collectors.toList());

System.out.println(result); // [ALICE]
```
