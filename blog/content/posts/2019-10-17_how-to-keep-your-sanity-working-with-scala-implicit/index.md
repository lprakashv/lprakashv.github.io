---
title: "How to keep your sanity working with Scala Implicit!"
author: "Lalit Vatsal"
date: 2019-10-17T08:14:10.190Z
lastmod: 2022-08-13T01:14:49+05:30

description: ""

subtitle: "Scala Implicits provide a lot of power and flexibility to express the code in such beautiful ways that development sometimes feel like and…"

image: "/posts/2019-10-17_how-to-keep-your-sanity-working-with-scala-implicit/images/1.jpeg"
images:
 - "/posts/2019-10-17_how-to-keep-your-sanity-working-with-scala-implicit/images/1.jpeg"
 - "/posts/2019-10-17_how-to-keep-your-sanity-working-with-scala-implicit/images/2.gif"
 - "/posts/2019-10-17_how-to-keep-your-sanity-working-with-scala-implicit/images/3.png"
 - "/posts/2019-10-17_how-to-keep-your-sanity-working-with-scala-implicit/images/4.png"
 - "/posts/2019-10-17_how-to-keep-your-sanity-working-with-scala-implicit/images/5.png"
 - "/posts/2019-10-17_how-to-keep-your-sanity-working-with-scala-implicit/images/6.gif"
 - "/posts/2019-10-17_how-to-keep-your-sanity-working-with-scala-implicit/images/7.gif"
 - "/posts/2019-10-17_how-to-keep-your-sanity-working-with-scala-implicit/images/8.gif"
 - "/posts/2019-10-17_how-to-keep-your-sanity-working-with-scala-implicit/images/9.png"


aliases:
    - "/how-to-keep-your-sanity-working-with-scala-implicit"
    - "/posts/how-to-keep-your-sanity-working-with-scala-implicit"

tags:
  - "scala"
  - "scala implicits"
  - "pimp my library pattern"
  - "clean code"
  - "scala patterns"

---

![image](/posts/2019-10-17_how-to-keep-your-sanity-working-with-scala-implicit/images/1.jpeg#layoutTextWidth)
Courtesy: [https://www.pexels.com/](https://www.pexels.com/photo/calm-daylight-evening-grass-267967/)

## Intro

Scala Implicits provide a lot of power and flexibility to express the code in such beautiful ways that development sometimes feel like and art and are nothing short of a “[Brahmastra](https://en.wikipedia.org/wiki/Brahmastra)” in the hand of a library developer.

And, as Spider-man’s uncle said,
> “With great power, comes greater responsibility!”

The abuse of such a powerful feature has made working with them a nightmare sometimes for the end users. For example:

![image](/posts/2019-10-17_how-to-keep-your-sanity-working-with-scala-implicit/images/2.gif#layoutTextWidth)

You will keep you head scratching over the above script until you find an implicit conversion (from Int to String) and an extension method (toHindiDigits) coming from just two imports!

![image](/posts/2019-10-17_how-to-keep-your-sanity-working-with-scala-implicit/images/3.png#layoutTextWidth)

![image](/posts/2019-10-17_how-to-keep-your-sanity-working-with-scala-implicit/images/4.png#layoutTextWidth)

Even [Martin Odersky](https://en.wikipedia.org/wiki/Martin_Odersky) ( 🙌), the creator of Scala has admitted that he has made quite a few mistakes with the Implicits while designing the Scala language 😱!

{{< youtube id="1h8xNBykZqM" >}}

While this can be really disheartening, this is not enough of a reason to move away from an amazing programming language, just because of a really abused feature! After all, there are other languages with much more horrible warts!

![image](/posts/2019-10-17_how-to-keep-your-sanity-working-with-scala-implicit/images/5.png#layoutTextWidth)
Courtesy: <https://me.me>

And JS is the most popular language right now 😉So, coming onto our topic, keeping the sanity of our mind! For that, we can follow some tips:

### Use an IDE

Personal choice, IntelliJ IDEA with Scala plugin.

Look at features from [JetBrain’s Scala plugin blog](https://blog.jetbrains.com/scala/):

You can show implicitly passed parameters in a function, using “show implicit hints” feature, so that there’ll be **_no surprises_** as what was passed:

![image](/posts/2019-10-17_how-to-keep-your-sanity-working-with-scala-implicit/images/6.gif#layoutTextWidth)

Similar example,

![image](/posts/2019-10-17_how-to-keep-your-sanity-working-with-scala-implicit/images/7.gif#layoutTextWidth)

![image](/posts/2019-10-17_how-to-keep-your-sanity-working-with-scala-implicit/images/8.gif#layoutTextWidth)

### Avoid implicit conversions/defs

This can become a complete nightmare if a String or any type gets converted to another on the fly without even telling us and we spend hours debugging the issue

Even Scala compiler will warn you if you use implicit conversion without a specific import ( **scala.language.implicitConversions** ):

![image](/posts/2019-10-17_how-to-keep-your-sanity-working-with-scala-implicit/images/9.png#layoutTextWidth)

So, the tip is, **_avoid implicit conversions at all costs_**. When you absolutely need a conversion in your code in a convenient manner, please use [implicit classes with extension method](https://medium.com/@lprakashv/making-ordinary-classes-rich-scala-ab7f991d690) like:

```scala
trait A
trait B

//avoid this:
//implicit def aToB(a: A): B = ???

//do this instead:
implicit class RichA(a: A) {
  def toB = ???
}

//use it like this:
val someA: A = ???
val someB: SomeB = someA.toB

//so that, this will be avoided:
//val someB: SomeB = someA
```

### Ditch the type inference and annotate the required types

Simple logic: Avoid surprises 😅 and let compilation fail on mismatches!

### Check the imports

Any underscore imports may contain implicit conversions, parameters and/or somewhat safe implicit classes.

## Conclusion

So, these were my highly opinionated rules to avoid surprises and headaches while working with Scala Implicit! They are really powerful tools for writing really awesome code, please use them, don’t abuse them :)
