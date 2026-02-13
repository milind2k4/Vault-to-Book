Links: [[10 Functional Interface]]
___
# Advanced Java Features

This file covers modern Java language enhancements and features introduced in recent versions (Java 7+).

## Try-with-resources

Introduced in Java 7, it simplifies resource management by automatically closing resources that implement the `AutoCloseable` interface.

```java
// The resource (fis) is automatically closed at the end
try (FileInputStream fis = new FileInputStream("test.txt")) {
    // read file
} catch (IOException e) {
    e.printStackTrace();
}
```

## Annotations

### Type Annotations (Java 8)

Annotations can be placed almost anywhere a type is used, not just on declarations. This is primarily used by plug-in type-checking tools to find bugs (e.g., `@NonNull`).

```java
List<@NonNull String> names = new ArrayList<>();
```

### Repeating Annotations (Java 8)

Allows the same annotation to be applied multiple times to a single declaration.

```java
@Schedule(day="Mon")
@Schedule(day="Fri")
class MyTask { }
```

## Java Module System (Java 9)

Also known as **Project Jigsaw**. It is used to organize large applications into modules.

- **Encapsulation**: Can hide entire packages.
- **Dependencies**: Explicitly defines what a module needs.
- **Descriptor**: Uses `module-info.java`.

```java
// module-info.java
module com.myapp.main {
    requires com.myapp.utils; // Depends on another module
    exports com.myapp.api;    // Makes this package public
}
```

## Diamond Syntax with Anonymous Classes (Java 9)

The diamond operator `<>` can be used with anonymous inner classes.

```java
List<String> list = new ArrayList<>() {
    // Anonymous subclass body
};
```

## Local Variable Type Inference (Java 10)

Allows the compiler to infer the type of a local variable from its initializer using the `var` keyword.

```java
var message = "Hello"; // Inferred as String
var map = new HashMap<String, Integer>(); // Inferred as HashMap
```

## Switch Expressions (Java 14)

An enhanced switch statement that can be used as an expression (returns a value).

- **Arrow Syntax (`->`)**: No fall-through, no `break` needed.
- **Yield**: Used to return a value from a block.

```java
String day = "SAT";
String type = switch (day) {
    case "MON", "TUE", "WED", "THU", "FRI" -> "Weekday";
    case "SAT", "SUN" -> "Weekend";
    default -> "Invalid";
};
```

## Records (Java 16)

A concise way to create immutable data carrier classes. The compiler automatically generates the constructor, getters, `equals`, `hashCode`, and `toString`.

```java
record Point(int x, int y) {}

Point p = new Point(10, 20);
System.out.println(p.x()); // 10
```

## Sealed Classes (Java 17)

Restricts which other classes or interfaces may extend or implement them.

- `sealed`: Declares the class is sealed.
- `permits`: Lists the allowed subclasses.

```java
sealed interface Shape permits Circle, Square {}

final class Circle implements Shape {}
final class Square implements Shape {}
```

## Text Blocks (Java 15)

Used to represent multi-line strings.

```java
String json = """
    {
        "name": "John",
        "age": 30
    }
    """;
```
