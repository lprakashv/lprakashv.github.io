---
title: "Cushing Design Patterns! — Unnecessary Patterns."
author: "Lalit Vatsal"
date: 2019-09-30T05:16:43.708Z
lastmod: 2022-08-13T01:14:47+05:30

description: ""

subtitle: "This is the part-II in the continuation of the “Crushing Design Patterns” series (Part-I) where we debunk the idea of having to use the…"

image: "/posts/2019-09-30_cushing-design-patternsunnecessary-patterns/images/1.jpeg"
images:
 - "/posts/2019-09-30_cushing-design-patternsunnecessary-patterns/images/1.jpeg"


aliases:
    - "/cushing-design-patterns-unnecessary-patterns"
    - "/posts/cushing-design-patterns-unnecessary-patterns"

tags:
  - "design patterns"
  - "java"
  - "scala"
  - "functional programming"
  - "FP"
  - "builder pattern"
  - "lambda functions"
  - "java streams"
  - "strategy pattern"
  - "command pattern"
  - "iterator pattern"

---

![image](/posts/2019-09-30_cushing-design-patternsunnecessary-patterns/images/1.jpeg#layoutTextWidth)

This is the part-II in the continuation of the “Crushing Design Patterns” series ([Part-I](../2019-09-26_crushing-design-patterns-with-scalachain-of-responsibility)) where we debunk the idea of having to use the design patterns to design the system.

## Intro

They are either just so natural that we have been using them unconsciously or there are better ways in which we don’t have to focus on ceremoniously writing them.Here we go.

### 1. Builder Pattern

> The intent of the Builder design pattern is to separate the construction of a complex object from its representation.> — Wikipedia

Meaning in plain english: _A way to create objects with a flexibility to use any number of parameters for its creation._

Question: what is wrong with the constructors?

{{< gist d26672d894bc16fa175f55ef308d6f35 2cde574aa004d277509e1b37d25a3b405ea17969 >}}

Actual video of me deciding which parameters to put in constructors

{{< video src="https://c.tenor.com/X_L4uaFnF0QAAAPo/bird-blocks.mp4" autoPlay=true loop=true id="bird-blocks.mp4" >}}

Counter question: How many would you make? To answer that, I’ll have show off my high school mathematics:
> If there are **_n_** optional parameters/fields, there will be **_2^n_** possible combinations of them, that means we’ll have to create those many constructors.

Turns out it will be 64 for our 6 optional veggies. Oh God, Java will make me die unhealthy!

{{< video src="https://c.tenor.com/7nksOF9d4XQAAAPo/cookie-monster-vegetables.mp4" autoPlay=true loop=true id="cookie-monster-vegetables.mp4" >}}

Here comes the Builder pattern for our rescue,

{{< gist lprakashv c739b9ebcbbcc06979711bed37ed0236 >}}

But hey, this is 2019 and remember, we don’t need to do it like this! Behold, Java has a saviour now, [**_lombok_**](https://projectlombok.org/features/all)**_!_** Let’s rewrite our lombok-y Sandwich class:

{{< gist lprakashv 47feb00c232296a0105c86ee3f911a55 >}}

{{< video src="https://c.tenor.com/8zE-Vg8zqV8AAAPo/jake-adventure-time.mp4" autoPlay=true loop=true id="jake-adventure-time.mp4" >}}

That is it! Heck, we didn’t even need write the getters and setters ourselves, lombok does it all for you ! How do we use it, if you ask. Simple:

{{< gist lprakashv 28770ff78553c0dc2578afc72c509641 >}}

> **Pro Tip:** If you are a Java dev, you should definitely check out the [**Project Lombok**](https://projectlombok.org/features/all), it offer dozens of cool modern features with simple annotations. **All the lombok annotated code simply de-sugars at the compile time into the ugly Java we don’t wanna write!**

**_Verdict: Builder Pattern is unnecessary in Java due to lombok! Some languages provide features like named and default arguments (Scala, Clojure, Python etc) making the object building easier._**

### 2. Iterator Pattern

> The**iterator pattern** is a design pattern in which an iterator is used to traverse a container and access the container’s elements. The iterator pattern decouples algorithms from containers.> — Wikipedia

Meaning: _It’s a pattern where_ **_an abstract container_** _providing a_ **_next()_** _method and in some cases hasNext() method as well._

{{ video src="https://c.tenor.com/H1P0_7Aq8vMAAAPo/next-britney-spears.mp4" autoPlay=true loop=true id="next-britney-spears.mp4" }}

At this point, if you are a programmer, your brain should be screaming right now. **We already have those in every mainstream programming language!!**.

* **Java** has **Iterator<T<** interface.
* **Python** objects provides ****next**()** method.
* **Scala and other functional languages** provide **sequences** and **lazy sequences**.

### 3. Command Pattern

> Here, object is used to encapsulate all information needed to perform an action or trigger an event at a later time.> — Wikipedia

Meaning: Every command implementation does what it is meant for!

{{< video src="https://c.tenor.com/gM3gv9qsN9MAAAPo/your-wish-is-my-command-geenie.mp4" autoPlay=true loop=true id="your-wish-is-my-command-geenie.mp4" >}}

{{< gist lprakashv c09c9975cc0828539c6e547ab10200e2 >}}

Usage:

{{< gist lprakashv c21f5e07a76638eae91bd7bde520b9dc >}}

You got the point right! Now, I want to you to pay attention and see that “_we only care about the encapsulated execute() method”_. So, in a nutshell, the **_Command pattern is just a function/method!_**

This becomes very intuitive with Java-8 lambdas, we don’t need to create LoginCommand and LogoutCommand wrapper implementations of the Command interface:

{{< gist lprakashv a79701e737154861496d6b172a993af7 >}}

BTW, this is very easy in functional languages, let’s take Scala for example:

{{< gist lprakashv d6f1bec5c5928acdcb9ba63e88e1fa47 >}}

### 4. Strategy Pattern

> S**trategy pattern** (also known as the **policy pattern**) enables selecting an algorithm at runtime. Instead of implementing a single algorithm directly, code receives run-time instructions as to which in a family of algorithms to use.> — Wikipedia

Meaning: **_Injecting the algorithm/strategy for some computation at runtime._**

For example, suppose we are running a country named LaLaLand and are running out of cash. What would be the best way to fill up our stash?

{{< video src="https://c.tenor.com/qcon77gJQxUAAAPo/taxes-tax.mp4" autoPlay=true loop=true id="taxes-tax.mp4" >}}

We start making a taxing strategy, let’s tax a quarter of the income of everybody.

```python
# quarter-taxing-strategy:
tax = user.income / 4
```

But , when we think about the good people running a kitten orphanage NGO, we feel bad for them. Also, we want to tax more the black money holders now. **We need more strategies**!

```python
# non-profit-taxing-strategy:
tax = 0
# half-taxing-strategy:
tax = user.income / 2
```

Here, **_the algorithm is the taxing strategy_** to compute the taxes from users. More strategies mean, more algorithms (functions). Let’s start with good old Java way:

{{< gist lprakashv 2156908af1a9a6f5f0321d287728b51a >}}

For every new strategy, we need to create another implementation class! Usage:

{{< gist lprakashv 6b49ae0861f6bfaec9295bb7e3bca424 >}}

Smart ones among you might already have guessed that **_we don’t need the wrapper implementation classes, we just need functions as strategies and pass them around arguments_**!

Let’s do it in functional way (no need to create multiple implementations of Strategy interface):

{{< gist lprakashv 594d5e7397e7dd2ec4fcaf80218195c6 >}}

{{< video src="https://c.tenor.com/HDaAEuOODc4AAAPo/cool-coolbeans.mp4" autoPlay=true loop=true id="cool-coolbeans.mp4" >}}

In functional languages (Scala):

{{< gist lprakashv ba85d532183912bf0fcf6f193c197b09 >}}

## Conclusion

We have discussed 4 pattern in this post: Builder, Iterator, Command and Strategy. Each one can be used without writing any pattern, simply by just intuitively using language features (even in Java). Each pattern has been right in front of us hiding in the language!

In summary:

1. _Builder — Lombok’s Builder annotation in Java, named and default parameters in other languages (Scala, Clojure, Python etc)._
2. _Iterator — Readily available interfaces/abstractions in many languages._
3. _Command — Just pure functions._
4. _Strategy — passing functions as strategy at runtime._
