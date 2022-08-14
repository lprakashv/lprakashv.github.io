---
title: "Making ordinary classes Rich! (Scala)"
author: "Lalit Vatsal"
date: 2019-10-07T17:24:21.805Z
lastmod: 2022-08-13T01:14:48+05:30

description: ""

subtitle: "How do we enrich something? By making it abundant, rich in features and resourceful! In simple OOP terms, we add additional feature methods to the class!!"

image: "/posts/2019-10-07_making-ordinary-classes-rich-scala/images/1.jpeg"
images:
 - "/posts/2019-10-07_making-ordinary-classes-rich-scala/images/1.jpeg"


aliases:
    - "/making-ordinary-classes-rich-scala-ab7f991d690"

tags:
  - "scala"
  - "scala implicits"
  - "pimp my library pattern"

---

![image](/posts/2019-10-07_making-ordinary-classes-rich-scala/images/1.jpeg#layoutTextWidth)

Let me break it to you, this post has nothing to do with charity! Now, let’s start with a question:
> **How do we enrich something?**

By making it abundant, rich in features and resourceful!

In simple OOP terms, we add additional feature methods to the class!!

Let’s try to enrich a Person class, starting with the basic class:

{{< script src="https://gist.github.com/lprakashv/802d185e9a3bdbebbf95da9ff8b44242.js" >}}

Now, to make a person speak French, we have to **add another method** to our Person class:

{{< script src="https://gist.github.com/lprakashv/7a20470c58ef5187c67e6696c5ae49e0.js" >}}

This is perfectly fine! Just add the additional feature to the existing class and make it rich.

But… **_there are cases when we cannot add features/methods to classes, like, library classes_** (java.util.Date, String, etc).

To add features to such classes we have to make **_“wrapper classes”_**. Suppose we want to add the “spell the digits” feature in the standard libraries Int class, we would have to make a wrapper class over Int.

{{< script src="https://gist.github.com/lprakashv/23463905122a10c1cdb32306c92ae101.js" >}}

Problem with this wrapper class approach is, if the desired class’ objects are used in a lot of places, then **_refactoring the class objects to our Rich-Wrapper class objects becomes a real pain!_**
> **Solution: Implicit classes and extension methods**

We will now make slight changes to our wrapper class:

1. Add an **_implicit_** keyword in front of the class.
2. Put the implicit class in a container object, which has a reason but also is generally a good practice. This way, we can import the “rich” feature at will!
3. Import contents of the container object.
4. Use the method on simple objects directly!

{{< script src="https://gist.github.com/lprakashv/7cbb9b7d81ee139ed33cdc3a2b394e7e.js" >}}

This pattern of creating an implicit class to enhance a library’s features has a funny name
> “Pimp My Library Pattern”

<!--adsense-inarticle-->

The example we shown above was a very basic example of Implicit class and its extension methods. The application of Implicit classes reach far beyond this!

One such example, is creating a generic method time profiler:

{{< script src="https://gist.github.com/lprakashv/85c214c605dca2f7a9359ca4f9e447e9.js" >}}

Then, what are your waiting for? Since, now you’ve learned to “pimp” any library, go make the mundane library objects rich with features you like!

{{< video src="https://c.tenor.com/qGM0NI-m_rgAAAPo/themoreyouknow-more.mp4" autoPlay=true loop=true id="themoreyouknow-more.mp4" >}}

_fin._
