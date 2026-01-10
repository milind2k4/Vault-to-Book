Links: [[01 Inheritance]]
___
# Polymorphism

"Many Forms"

Polymorphism is an OOP mechanism where an object (or method) can take on many different forms. Its main advantage is code reusability and flexibility.

> [!TIP] > Analogy: One Person, Many Roles
> Consider a man named **John**.
>
> - At home, he behaves as a **Father**.
> - At work, he behaves as an **Employee**.
> - At the store, he behaves as a **Customer**.
>
> **John** is the same object, but his behavior changes based on the context (who is interacting with him). This is Polymorphism.

It is achieved by two ways:

- **Compile-Time Polymorphism (Static Binding):** Achieved via **Method Overloading**.
- **Run-Time Polymorphism (Dynamic Binding):** Achieved via **Method Overriding**.

### Compile-Time Polymorphism (Method Overloading)

When a class has multiple methods with the same name but different parameters, it is known as method overloading. The correct method to call is decided at **compile-time** based on the arguments provided.

Method overloading is distinguished by:

- The **no. of parameters**
- The **datatypes** of parameters
- The **sequence** of parameters of different types

**Note:** The return type alone is **not** enough to overload a method.

```java
class Calculator {
    void add(int a, int b) {
        System.out.println(a + b);
    }

    void add(int a, int b, int c) { // Different no. of parameters
        System.out.println(a + b + c);
    }

    void add(double a, double b) { // Different datatypes
        System.out.println(a + b);
    }
}
```

#### Constructor Overloading

We can also overload constructors in the same way to provide different ways of initializing an object.

```java
class A {
    A(){
        // non-parameterized constructor
    }
    A(int a){
        // parameterized constructor
    }

    // To call a constructor from another constructor in the same class:
    A(int a, int b) {
        this(a); // 'this()' calls another constructor
        // ...
    }
}
```

### Run-Time Polymorphism (Method Overriding)

When a method in a **subclass** has the same name, parameters, and return type as a method in its **superclass**, it is known as method overriding.

This is also known as dynamic polymorphism because the actual method call is resolved at **run-time**, based on the type of the _object_, not the type of the _reference_.

This requires an "IS-A" relationship ([[01 Inheritance]]).

#### Rules for Method Overriding

- The method signature (name and parameters) must be identical.
- The return type must be the same or a _covariant_ type (a subclass of the original return type).
- The access modifier in the child class must be the same or _less restrictive_ (e.g., `protected` in parent can be `public` in child, but not `private`).
- `final` or `static` methods cannot be overridden.

#### Dynamic Method Dispatch

This is the mechanism that makes run-time polymorphism work. We can use a parent class reference to hold a child class object.

```java
class Animal { // Parent class
    void sound() {
        System.out.println("Animal makes a sound");
    }
}

class Dog extends Animal { // Child class
    @Override
    void sound() {
        // 'super' keyword calls the parent's method
        // super.sound();
        System.out.println("Woof! Woof!");
    }
}

class Cat extends Animal { // Child class
    @Override
    void sound() {
        System.out.println("Meow!");
    }
}

public class Main {
    public static void main(String[] args) {
        Animal a; // Parent class reference

        a = new Dog(); // Dynamic Polymorphic Assignment
        a.sound();     // Output: Woof! Woof! (Java checks the object type at run-time)

        a = new Cat(); // Re-assign to another subclass
        a.sound();     // Output: Meow! (Java checks the object type again)
    }
}
```

Here, even though the reference `a` is of type `Animal`, the JVM calls the `sound()` method from the _actual object_ (`Dog` or `Cat`) at run-time.
