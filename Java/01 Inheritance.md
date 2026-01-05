Links:

---

# Inheritance

Inheritance is a mechanism where one class acquires the properties and behaviors (methods) of another class.
This creates an "IS-A" relationship (e.g., a `Dog` IS-A `Animal`).

We need at least 2 classes.
We use `extends` keyword to inherit properties from one class to another.

The class which is inherited is called Parent or Super class.
The class which inherits is called Child, Derived or Sub Class.

> [!TIP] > Analogy: DNA & Genetics
>
> - **Parent Class:** Your Father. He has blue eyes (Properties) and walks fast (Behavior).
> - **Child Class:** You. You _automatically_ get the blue eyes and fast walk (Inheritance).
> - **Extending:** You can also learn to play guitar (New Method), which your father couldn't do. You are an "extension" of him.

Private properties and methods (`private`) are _not directly accessible_ by the child class, but they are still part of the object's structure.
Protected (`protected`) and `default` (package-private) members are inherited and accessible within the same package. `protected` members are also accessible to subclasses in different packages.

```java
class A { // Parent / Super class
    int a = 10;

    int func(){
        return 10;
    }

    private int privateFunc(){
        return 55;
    }
}

class B extends A { // Child / Sub class
    void test() {
        System.out.println(a); // Works
        System.out.println(func()); // Works
        // System.out.println(privateFunc()); // Error: privateFunc() has private access in A
    }
}
```

Here, B is child class and A is parent class.

### Types of Inheritance

#### Single Level

When one class inherits another. (A -> B)

```java
class A {}

class B extends A {}
```

#### Multi Level

When one class inherits another, which in turn inherits from another class. (A -> B -> C)

```java
class A {}

class B extends A {}

class C extends B {}
```

#### Hierarchical

When many classes inherit one single class. (A -> B, A -> C)

```java
class A {}

class B extends A {}

class C extends A {}
```

#### Multiple

When one class inherits from many classes.

Java does not allow for multiple inheritance using classes. This is to avoid the "Diamond Problem" (ambiguity if two parent classes have a method with the same name).

We must use interface to achieve this.

```java
class A {}

class B {}

// class C extends A,B {} // This does not work. Compilation Error.
```

#### Hybrid

When we use more than one kind of inheritance at the same time.

Java's class inheritance is hybrid, but without Multiple inheritance. A common example is Hierarchical + Multi Level.

```java
class A {} // Grandparent

class B extends A {} // Parent 1

class C extends B {} // Child (Multi-level)

class D extends A {} // Parent 2 (Hierarchical)
```

### Method Overriding

When a child class provides a specific implementation for a method that is already defined in its parent class.

The method signature (name, parameters) must be the same.

The @Override annotation is used to tell the compiler we intend to override a method.

```java
class Animal {
    void makeSound() {
        System.out.println("Generic animal sound");
    }
}

class Dog extends Animal {
    @Override
    void makeSound() {
        System.out.println("Woof");
    }
}
```

### `super` Keyword

`super` is a reference variable used within a child class to refer to the immediate parent class object.

It is used in two ways:

1. To call the super class's constructor.
2. To access the super class's members (variables or methods).

```java
super.member // e.g., super.variable, super.method()
super()      // e.g., super(), super(parameter)
```

The first one is used for calling the super class's members. This is most useful when a child class has overridden a method and needs to call the parent's version.

The second one is used for calling the super class's constructor.

- `super()` _must_ be the first statement in a child class's constructor.
- If you do not explicitly call `super()`, the compiler automatically inserts a call to the parent's non-parameterized `super()` constructor.

```java
class Parent {
    String name;

    Parent(String name) {
        this.name = name;
    }

    void print() {
        System.out.println("Parent print");
    }
}

class Child extends Parent {
    Child(String name) {
        // Must call super() because Parent has no default constructor
        super(name);
    }

    @Override
    void print() {
        super.print(); // Calls Parent's print() method
        System.out.println("Child print");
        System.out.println(super.name); // Accesses Parent's variable
    }
}
```
