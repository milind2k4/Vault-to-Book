Links: [[14 Spring Framework]]

---

# Spring Boot

Spring Boot is an extension of the Spring Framework that simplifies the setup and development of new Spring applications.

**Key Features:**

- **Auto-Configuration**: Automatically configures Spring based on jar dependencies.
- **Standalone**: Embeds Tomcat, Jetty, or Undertow directly (no need to deploy WAR files).
- **Starter Dependencies**: Simplified build configuration (e.g., `spring-boot-starter-web`).
- **Production-ready**: Metrics, health checks, externalized configuration.

## Difference between Spring and Spring Boot

| Feature           | Spring Framework                           | Spring Boot                                             |
| :---------------- | :----------------------------------------- | :------------------------------------------------------ |
| **Goal**          | Provides infrastructure for building apps. | Simplifies booting and development.                     |
| **Configuration** | Manual (XML or Java-based).                | **Auto-configuration** (Convention over Configuration). |
| **Server**        | External server required (e.g., Tomcat).   | **Embedded server** (Tomcat/Jetty) included.            |
| **Dependency**    | Dependencies managed manually.             | **Starters** simplify dependency management.            |
| **Boilerplate**   | Significant boilerplate code.              | Reduces boilerplate code drastically.                   |

## Build Systems

Spring Boot projects typically use **Maven** or **Gradle**.

- `pom.xml` (Maven)
- `build.gradle` (Gradle)

## Code Structure

```java
com
 +- example
     +- myapp
         +- Application.java (Main Class)
         |
         +- domain (Entities)
         +- repository (DAO)
         +- service (Business Logic)
         +- web (Controllers)
```

## Spring Boot Runners

Interfaces used to run code _after_ the application starts.

1.  **CommandLineRunner**: `run(String... args)`
2.  **ApplicationRunner**: `run(ApplicationArguments args)`

## Logging

Spring Boot uses Commons Logging for all internal logging but leaves the underlying log implementation open. Default is **Logback**.

```java
Logger logger = LoggerFactory.getLogger(MyClass.class);
logger.info("This is an info message");
```

## RESTful Web Services

**REST** (Representational State Transfer) is an architectural style for web services.

### Annotations

- `@RestController`: Combines `@Controller` and `@ResponseBody`.
- `@RequestMapping`: Maps HTTP requests to handler methods.
- `@RequestBody`: Maps the HTTP request body to a Java object.
- `@PathVariable`: Extracts values from the URI path.
- `@RequestParam`: Extracts query parameters.

### HTTP Methods

| Method     | Annotation       | Purpose                                    |
| :--------- | :--------------- | :----------------------------------------- |
| **GET**    | `@GetMapping`    | Retrieve a resource.                       |
| **POST**   | `@PostMapping`   | Create a new resource.                     |
| **PUT**    | `@PutMapping`    | Update an existing resource (full update). |
| **DELETE** | `@DeleteMapping` | Delete a resource.                         |

### Example Controller

```java
@RestController
@RequestMapping("/api/users")
public class UserController {

    // GET /api/users/1
    @GetMapping("/{id}")
    public User getUser(@PathVariable int id) {
        return new User(id, "John");
    }

    // POST /api/users
    @PostMapping
    public User createUser(@RequestBody User user) {
        // save user...
        return user;
    }

    // GET /api/users?role=admin
    @GetMapping
    public List<User> getUsers(@RequestParam(defaultValue = "user") String role) {
        // return users by role...
        return new ArrayList<>();
    }
}
```
