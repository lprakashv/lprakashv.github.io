---
title: "Crushing Design Patterns with Scala! — Chain of responsibility"
author: "Lalit Vatsal"
date: 2019-09-26T06:06:23.463Z
lastmod: 2022-08-13T01:14:45+05:30

description: ""

subtitle: "In this (and hopefully further upcoming series) post, we will debunk the idea of really needing to use the Design Patterns. I believe that…"

image: "/posts/2019-09-26_crushing-design-patterns-with-scalachain-of-responsibility/images/1.jpeg"
images:
 - "/posts/2019-09-26_crushing-design-patterns-with-scalachain-of-responsibility/images/1.jpeg"
 - "/posts/2019-09-26_crushing-design-patterns-with-scalachain-of-responsibility/images/2.gif"


aliases:
    - "/crushing-design-patterns-with-scala-chain-of-responsibility"
    - "/posts/crushing-design-patterns-with-scala-chain-of-responsibility"

tags: ['design patterns', 'java', 'scala', 'chain of responsibility']

---

![image](/posts/2019-09-26_crushing-design-patterns-with-scalachain-of-responsibility/images/1.jpeg#layoutTextWidth)

**_Starting this chain of responsibility of debunking the idea of really needing to use the_**[**_Design Patterns_**](https://en.wikipedia.org/wiki/Design_Patterns)**_!_**. I believe that design patterns were created to standardise the OO patterns needed to solve the common problems arising due to not having a standard way of solving them using the programming language itself.
> Design patterns should be used only as communication tool and not the way we have been using as a design tool. — Mr. [Venkat Subramaniam](https://twitter.com/venkat_s)

Coming on to our language, **Scala, being a multi-paradigm programming language gets the goodness of both functional and OO worlds**. This is truly visible with the functional magic being applied in the OO design patterns.

We will start with our pattern “Chain of Responsibility”, its definition says:
> In object-oriented design, the **chain-of-responsibility pattern** is a design pattern consisting of a source of command objects and a series of processing objects. Each processing object contains logic that defines the types of command objects that it can handle; the rest are passed to the next processing object in the chain. A mechanism also exists for adding new processing objects to the end of this chain> - Wikipedia
![image](/posts/2019-09-26_crushing-design-patterns-with-scalachain-of-responsibility/images/2.gif#layoutTextWidth)

**_To put it simply, the chain of responsibility pattern can be considered as an assembly line, each processing unit doing their own part and then passing the other processing units._**

Let’s consider a problem to solve. Consider You want to filter out (beep) profanity out of a public chat system (_This example is inspired from Mykhailo Kozik’s post_ [**_Clojure Design Patterns_**_._](http://mishadoff.com/blog/clojure-design-patterns/#episode-16-chain-of-responsibility)).

Further more, you would only want to _beep_ the profanity coming from a certain respectable person. You can leave the rest of the world with their freedom of expression ;)

Consider your chat stream looks something like this:

```txt
#format: [user] comment

[Suresh01] Hello!
[RameshXX] Hi Suresh, how are you.
[TheMostRejectableGuyInTown] Yo wazzup people.
[Suresh01] Not you again Ramesh! curse you!
[MrRespectable007] curse all of you, I curse the world!!
```

You would now want to extend this a little further and wanna have provision to log, reject and _beep_ out (transform) certain words.

Solution:

Simple! We just need to filter the sh*t out of everything.

Let me talk a bit in Java now, _we will create a Filter abstraction and create Rejector, Moderator, Logger etc implementations of it._

Abstraction for the Filter:

{{< gist fd7dd335418f3a2b7faeb0ef8deaa3d2 1bb5c74e79ae83fdc26c2fbcb09423cfebbc5b12 >}}

Implementations of the Filter:

{{< gist ac1df3e6a1b04aad4769a570fa4f0af4 0a79c91841c22a60b54f3599697aa346ca87ba3e >}}

Wow, that was some effort for such a simple task!

Now, let’s use the filters chained to work together in the order we define.

{{< gist f6ce039c1f1960faa45e3261124722db 928308d0f6e75540cf48460d7cd6e84da29c1170 >}}

We could do the exact same thing with Scala too, well, it doesn’t restrict (or force) you from doing what you want! You are free to jump in your own created well.

If we take a step back and look at the pattern (or rather problem) again, we could see that **_we just care about the process method and the order in which they are applied._**

Since, **functions are the first class citizens in Scala**, we could argue that we just want the methods and not the entire Filter classes, and some way of composing them.

Voila, we have our answer here, **“functional composition”** using **_andThen_**.

```scala
/* For single argument function, andThen method signature looks like */
trait Function1[-T1, +R] {
  def apply(v1: T1): R
  def andThen[A](g: R =< A): T1 =< A = { x =< g(apply(x)) }
}
```

_In plain english, it takes function with input type the same as the return type of the current function it is applied on (R) and returning a new type (A) value. andThen passes the result of the current function to the function passed in and then returns output of the passed function._

Some syntactic sugar in Scala:

```scala
a.method(b.innerMethod(c)
/* is equivalent to */
a method (b innerMethod c)

a.method1(b).method2(c)
/* is equivalent to */
a method1 b method2 c
```

Now, using all our magic here,

{{< gist a8a82dd6ef7d5f1813e3e813a087f0e8 1c179fd7582da567da4aff9831026a95eaec2a98 >}}

Pretty neat huh! Remember, there is no magic just some hard work behind the scenes. In our case, it’s the Scala compiler.

## Conclusion

In conclusion, we shouldn’t have to worry about writing tedious patterns for standard well known problems if the language itself provides them out of the box! We could just take a break from the computer screen and say “Hello world!” literally, in the time we save :)

{{< figure src="https://c.tenor.com/FxCJGKCeVBIAAAAC/take-a-break-break.gif" >}}

Thank you! And here is [Part-II](../2019-09-30_cushing-design-patternsunnecessary-patterns).
