Links:
___
# Encapsulation
It is a fundamental OOP principle used for **data hiding**.
Encapsulation is a mechanism in which data (attributes or variables) and the methods that operate on that data are bundled together within a single unit (a class).

We make a "capsule" of a class. What's inside the capsule (the internal state) is not available for direct access from outside the class.

Attributes are bound to the methods. We cannot get or set the values of the attributes directly by doing `obj.var`. We must use accessor methods like `obj.getVar()` (a **getter**) or `obj.setVar(value)` (a **setter**).

Encapsulation provides:
- **Data Hiding (Security):** The internal state of the object is hidden. This prevents outside code from accidentally or maliciously corrupting the object's data.
- **Control & Data Integrity:** By using setter methods, we can add validation logic. Data remains authentic because we control *how* it is set.
- **Flexibility & Modularity:** The implementation details are hidden. We can change the internal implementation (e.g., rename a variable, change its data type) without breaking the external code that uses our class, as long as the public getter/setter methods remain the same.
- **Code Reusability:** Encapsulated classes are easier to reuse as self-contained "black boxes."

### How to Achieve Encapsulation
1.  Declare the class's variables (fields) as `private`.
2.  Provide public **getter** (accessor) methods to view the variables.
3.  Provide public **setter** (mutator) methods to modify the variables.

Setters are where we enforce integrity constraints.

For example:
```java
class Student {
    // 1. Declare variable as private
    private int age;
    
    // 3. Public setter to initialize/modify the variable
    public void setAge(int age) {
        // We add validation logic (integrity constraint)
        if (age > 0 && age < 150) {
            this.age = age;
        } else {
            System.out.println("Invalid age provided.");
            // Or throw new IllegalArgumentException("Invalid age");
        }
    }
    
    // 2. Public getter to access the variable
    public int getAge() {
        return this.age;
    }
}

class Main {
    public static void main(String[] args) {
        Student s1 = new Student();
        
        // s1.age = -10; // Error: 'age' has private access
        
        s1.setAge(20);
        System.out.println(s1.getAge()); // Output: 20
        
        s1.setAge(-10); // Output: Invalid age provided.
        System.out.println(s1.getAge()); // Output: 20 (The value didn't change)
    }
}
````

The encapsulation is:
- **Read-Only:** If we only provide a `getter`, the variable becomes read-only from the outside.
- **Write-Only:** If we only provide a `setter`, the variable becomes write-only.