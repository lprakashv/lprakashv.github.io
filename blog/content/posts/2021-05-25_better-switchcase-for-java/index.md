---
title: "Better Switch-Case for Java!"
author: "Lalit Vatsal"
date: 2021-05-25T11:30:29.891Z
lastmod: 2022-08-13T01:14:58+05:30

description: ""

subtitle: "Advanced Pattern matching in Java using “patternmatcher4j”"

image: "/posts/2021-05-25_better-switchcase-for-java/images/1.png"
images:
 - "/posts/2021-05-25_better-switchcase-for-java/images/1.png"
 - "/posts/2021-05-25_better-switchcase-for-java/images/2.png"
 - "/posts/2021-05-25_better-switchcase-for-java/images/3.png"
 - "/posts/2021-05-25_better-switchcase-for-java/images/4.png"
 - "/posts/2021-05-25_better-switchcase-for-java/images/5.png"
 - "/posts/2021-05-25_better-switchcase-for-java/images/6.png"


aliases:
    - "/better-switch-case-for-java-b3b09f14cebc"

tags:
  - "java"
  - "java streams"
  - "functional programming"
  - "FP"
  - "pattern matching"
  - "switch case"

---

![image](/posts/2021-05-25_better-switchcase-for-java/images/1.png#layoutTextWidth)

Let’s start with the question, what is wrong with the switch-case anyway? Here’s a simple example of a switch-case in Java:

![image](/posts/2021-05-25_better-switchcase-for-java/images/2.png#layoutTextWidth)

Can you see the problem here? It is the unnecessary “ceremony” of writing the “break” statement on each case!

You can argue that we can just return after each case-block, while this is a brilliant idea but, then the ceremony would be of writing “return” in each block 😜 you can even miss that!

In fact, the return statement at every case-block means that every block should **always** “return” or “evaluate” to something! Which is the most fundamental idea in Functional Programming, where **_every expression must return or evaluate something_** just like a mathematical “function”.

```text
value := **F(x)** <--- always returns a value!
```

In, fact this switch-case with always returning case blocks is omnipresent in all the FP languages as **“Pattern Matching”**, here is a simple determistic example code in Clojure:

![image](/posts/2021-05-25_better-switchcase-for-java/images/3.png#layoutTextWidth)

Some languages like Scala, Haskell take this idea even further to allow partial match or even destructured matches on the input argument:

![image](/posts/2021-05-25_better-switchcase-for-java/images/4.png#layoutTextWidth)

Enough features of other languages now! Now let’s come back to our hero here “**JAVA**”, can we do similar things in Java?
> Yes and No.

The standard library doesn’t have any similar feature but there are a few libraries supporting this, one among those is [**Vavr**](https://docs.vavr.io/#_pattern_matching) check it out!

However, I am going to shamelessly endorse my own library for this [job: **“patternmatcher4j”**](https://github.com/lprakashv/patternmatcher4j). **** You can start by adding the dependency:

**_Maven:_**

```xml
<dependency>
    <groupId>io.github.lprakashv</groupId>
    <artifactId>patternmatcher4j</artifactId>
    <version>0.2.0</version>
</dependency>`
```

**_Gradle:_**

```gradle
implementation 'io.github.lprakashv:patternmatcher4j:0.2.0'
```

Here is our simple case-match with the enum:

![image](/posts/2021-05-25_better-switchcase-for-java/images/5.png#layoutTextWidth)

Now, let’s see some advanced match-cases:

![image](/posts/2021-05-25_better-switchcase-for-java/images/6.png#layoutTextWidth)

Ins’nt this awesome? Short explanation of the library code-test above:

**PMatcher<T, R>:**

This is like an actual switch-case block, we initialize it using a constructor taking an object to be matched. This is a parameterized class where T = input matched object type and R = return type of the block.

**Match Cases:**

We can create a match-case using:

1. `.matchValue(value)` — to match the matched-object with the passed value using Java’s **_equals()_** method,
2. `.matchRef(ref)` — to matched the reference of the original matched-object with the passed ref.
3. `.matchCase(..)` — advanced matching!

**Advanced matchCase():**

We can match using 3 different types of cases:

1. Predicate match: To match the matched-object using a predicate. — `.matchCase(p -> methodReturningBoolean(p))`
2. Class match: To match the class of the matched-object — `.matchCase(SomeClass.class)`
3. De-structured match: To match matched-object’s fields (which internally uses Reflection API). _You can even use the recursive match with the_ **_MField_** _objects passed to the matchCase passing any of predicate, class, further de-structured matches_— `.matchCase(MField.with("field1", ...), MField.withValue("field2", field2Value), MField.with("field3", Field3.class))`

**Actions:**

Each of the matchCase, matchValue and matchRef produces an object of class “CaseActionAppender” which has 3 “action” methods which you can use to define action on the preceding match-case.

1. `.thenReturn(R returnValue)` — to return the value on the preceding match-case.
2. `.thenSupply(Supplier<R> supplier)` — to evaluate the return value lazily using a supplier.
3. `.thenTransform(Function<T,R> fn)` — to evaluate the return value by performing transformation operation on the matched-object.

<!--adsense-inarticle-->

## Fin

Please use the library and provide your valuable feedback, you can even raise a PR and I will look into it. This was my very first maven-central deployment so any suggestion will be welcomed :)

Thanks for reading!
