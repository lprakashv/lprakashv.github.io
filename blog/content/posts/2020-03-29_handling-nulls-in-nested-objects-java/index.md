---
title: "Handling Nulls in nested objects (Java)"
author: "Lalit Vatsal"
date: 2020-03-29T09:14:32.730Z
lastmod: 2022-08-13T01:14:51+05:30

description: ""

subtitle: "Handling NullPointerException and keeping track of all the nullable values has always been a pain for Java developers."

image: "/posts/2020-03-29_handling-nulls-in-nested-objects-java/images/1.png"
images:
 - "/posts/2020-03-29_handling-nulls-in-nested-objects-java/images/1.png"
 - "/posts/2020-03-29_handling-nulls-in-nested-objects-java/images/2.png"


aliases:
    - "/handling-nulls-in-nested-objects-java"
    - "/posts/handling-nulls-in-nested-objects-java"

tags:
  - "java"
  - "nulls"
  - "null pointer exception"
  - "error handling"
  - "java 8"
  - "java streams"

---

![image](/posts/2020-03-29_handling-nulls-in-nested-objects-java/images/1.png#layoutTextWidth)

Handling NullPointerException and keeping track of all the nullable values has always been a pain for Java developers.

This is even worse when you are working with deeply nested objects and handling all the null values grows exponentially with each nullable nested value. This is visible by all the statements like:

```java {style=github-dark}
if (x.y().z().. != null) {…}
```

In this article, we will explore some of the techniques starting with the naive approach to a more advanced one for handling such scenarios.So, are you ready? Let’s dive in…

Suppose we have a simple but nested object structure like:

```config {style=github-dark}
root {
  first-level {
    second-level {
      third-level {
        name: "string"
      }
    }
  }
}
```

where each object and/or value can be nullable. Say our objective is to create a greeting for the name nested three level deep behind root object.

Here are our test objects with our testing code:

{{< gist lprakashv 57284252c43370da7a47fe2a361d43ef >}}

Let’s start with the solutions:

### **Unsafe Approach:**

{{< gist lprakashv 38af049e1d4971a31a7cd8a394fd1b74 >}}

This can result in a NullPointerException!

Result:

```log {style=github-dark}
Failed to greet for r1 !
Failed to greet for r2 !
Failed to greet for r3 !
Greeting for r4 : Hello null
Greeting for r5 : Hello Lalit
```

### **Naive Safe Approach:**

{{< gist lprakashv f68f7f55cb60e42562a0e47a594c856f >}}

Result:

```log {style=github-dark}
Greeting for r1 : Hey There!
Greeting for r2 : Hey There!
Greeting for r3 : Hey There!
Greeting for r4 : Hey There!
Greeting for r5 : Hello Lalit
```

Look at the indentation increasing with the increasing nesting level. Although, we could combine the null checks, but if we wanted to do other operation on each nested object then we would have to adopt the above approach.

### **The Optional Approach**

{{< gist lprakashv 71d96300fb967d53825895b32351c1f7 >}}

Now, we will jump into the functional territory to solve this problem. Java 8’s Optional<T< comes to our rescue:

This works like a charm! The only problem is we cannot control and determine which stage failed or is null, and cannot have failover for each stage.

To implement that in Optional, we have to do like:

{{< gist lprakashv 5e446053cd0c236aca7d496fa987642e >}}

Result:

```log {style=github-dark}
Greeting for r1 : Hello first level is null
Greeting for r2 : Hello second level null
Greeting for r3 : Hello third level is null
Greeting for r4 : Hey There!
Greeting for r5 : Hello Lalit
```

This will work, but we had to write a lot of orElse statements to handle a particular null case and we have to be careful as to where we want to put them.

What if there was a way to pass a default at each map stage…?

### **Custom Wrapper Approach**

Let’s write our own NullableWrapper with mapper taking a default value at each map stage (We’ll consider null otherwise). Let’s call our object as NullableWrapper<T< which:

1. Takes a **supplier** returning a value of type T (denoting lazy computation) or a value of type T.
2. **May take** a **default value** of type T (if the supplier or value results in null) which is by default set to null.
3. Can **map** the current wrapper<T< to new wrapper<R< by providing a transforming function Function<T,R< and **may take** a **new default value** of type R which is otherwise set to null.
4. Can **get** the value by providing a **new default value** of type T which is otherwise set to null.

Now we have all the ingredients for the recipe, let’s start cooking!

{{< gist lprakashv 9c8b6e5db3c96f992724159524f2a36d >}}

Now, let’s taste it! I mean test it with the **mapWithDefault** feature (the other map will work exactly like Optional).

{{< gist lprakashv d92be758bbffd36928f9330d6ea5f150 >}}

This will also work just like we expected, and the code looks more elegant.

One more benefit of this is that **we don’t have to use the getOrElse every time as NullableWrapper’s .get() will return a default value or null** (in case default not provided) instead of blowing up:

```java {style=github-dark}
// will blow up!
Optional.ofNullable(null).map(x -> "Hello " + x).get();

// will return null
new NullableWrapper(() -< null).map(x -> "Hello " + x).get();
```

Now, let’s see the NullableWrapper<<() from the point of view of a library user. It asks for a supplier or a value of type T and a default value.

This makes me think that the **supplier evaluation must also be safe** as it would be lazily evaluated inside the wrapper! Let’s try it out:

{{< gist lprakashv 8132c283fc608077bbbb6835d3d71773 >}}

Result:

![image](/posts/2020-03-29_handling-nulls-in-nested-objects-java/images/2.png#layoutTextWidth)

Uh oh! What happened there?

This means the .get() operation is not that safe as we thought! How to make it safe? Let’s try to fix this by gulping all the NPEs:

{{< gist lprakashv 9333bc660e955883cbc61167a289aad4 >}}

Now, we also want to do mapping by ignoring NPEs:

{{< gist lprakashv 959dda9f696f099105ebc22f9054cb8a >}}

Let’s try that again:

{{< gist lprakashv 36fcc9f772c38b0b5ef05c6852b031a5 >}}

Result:

```log {style=github-dark}
Hey There!
Hi Lalit
```

## Conclusion

We saw how we can utilise the power of Optionals and functional programming concepts to get the safety of the null checks as well as the control over the outcome with a default value.

Our own NullableWrapper gives following advantages over builtin Optional:

* Mapping with a default value at any stage.
* Defining initial default value.
* Super safe lazy computation by ignoring NPEs.
* Safer than NullableWrapper’s get() is more safer than Optional’s get() as it will return null or a default value as the final result and won’t just blow up.

Hope you liked it. Thanks for reading :)
