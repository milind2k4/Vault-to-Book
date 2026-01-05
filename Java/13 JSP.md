Links: [[13.5 Servlets]]

---

# Java Server Pages (JSP)

JSP is a server-side technology used to create dynamic web content. It is an extension of Servlets.
JSP files are compiled into Servlets by the container.

## JSP Life Cycle

1.  **Translation**: JSP -> Servlet (.java)
2.  **Compilation**: Servlet -> Bytecode (.class)
3.  **Loading & Initialization**: `jspInit()`
4.  **Execution**: `_jspService()`
5.  **Destruction**: `jspDestroy()`

## Scripting Elements

1.  **Scriptlet Tag** `<% ... %>`: Contains Java code.
    ```jsp
    <% int count = 0; out.println(count); %>
    ```
2.  **Expression Tag** `<%= ... %>`: Prints a value (no semicolon).
    ```jsp
    <%= "Hello " + name %>
    ```
3.  **Declaration Tag** `<%! ... %>`: Declares methods or variables.
    ```jsp
    <%! int square(int n) { return n*n; } %>
    ```

## Implicit Objects

Objects created by the container and available automatically.

1.  **request**: `HttpServletRequest`
2.  **response**: `HttpServletResponse`
3.  **out**: `JspWriter` (for sending output)
4.  **session**: `HttpSession`
5.  **application**: `ServletContext`
6.  **config**: `ServletConfig`
7.  **pageContext**: Context for the page
8.  **page**: `this` (current servlet instance)
9.  **exception**: `Throwable` (only in error pages)

## Directives

Instructions to the container. Syntax: `<%@ directive ... %>`

1.  **page**: Defines page settings.
    ```jsp
    <%@ page language="java" contentType="text/html" import="java.util.*" %>
    ```
2.  **include**: Includes a file at translation time (static).
    ```jsp
    <%@ include file="header.jsp" %>
    ```
3.  **taglib**: Defines tag libraries (like JSTL).
    ```jsp
    <%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
    ```

## Standard Actions

XML tags to perform common tasks.

1.  **jsp:include**: Includes a resource at request time (dynamic).
    ```jsp
    <jsp:include page="footer.jsp" />
    ```
2.  **jsp:forward**: Forwards request to another page.
    ```jsp
    <jsp:forward page="login.jsp" />
    ```
3.  **jsp:useBean**: Instantiates a JavaBean.
    ```jsp
    <jsp:useBean id="user" class="com.example.User" />
    <jsp:setProperty name="user" property="name" value="John" />
    ```
