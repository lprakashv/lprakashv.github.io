---
title: "Going Reactive!"
author: "Lalit Vatsal"
date: 2020-04-16T10:47:47.735Z
lastmod: 2022-08-13T01:14:55+05:30

description: ""

subtitle: "There is a lot of hype around this shiny new thing in web applications development world called being “Reactive”! There are many…"

image: "/posts/2020-04-16_going-reactive/images/1.png"
images:
 - "/posts/2020-04-16_going-reactive/images/1.png"
 - "/posts/2020-04-16_going-reactive/images/2.gif"
 - "/posts/2020-04-16_going-reactive/images/3.png"
 - "/posts/2020-04-16_going-reactive/images/4.png"
 - "/posts/2020-04-16_going-reactive/images/5.png"
 - "/posts/2020-04-16_going-reactive/images/6.png"


aliases:
    - "/going-reactive"
    - "/posts/going-reactive"

tags:
  - "reactive programming"
  - "reactive applications"
  - "threadpool"
  - "executors"
  - "event loop"
  - "reactivex"
  - "reactive framework"

---

![image](/posts/2020-04-16_going-reactive/images/1.png#layoutTextWidth)
Logo courtesy: [http://reactivex.io/](http://reactivex.io/)

There is a lot of hype around this shiny new thing in web applications development world called being “Reactive”! There are many frameworks popping up with this slogan, e.g., Vert.x, Akka, Spring Webflux, Play, RxJava, RxJS etc. to name a few. What does it mean? and why is this hype? is it worth your time? Let’s explore…

### What does Reactive mean exactly?

Being reactive means **_ability to “react” to “events/changes”._** One very simple example is how a column in excel-sheet gets updated (reacts) if the column which it depends upon changes.

![image](/posts/2020-04-16_going-reactive/images/2.gif#layoutTextWidth)

This is a known design pattern and **_can be implemented using “Observer pattern” or a “Publisher-Subscriber pattern”_**, where there is a publisher and one or more subscribers to it.

There are two distinct things which are Reactive, [a] **Reactive programming**, which uses the reactive programming principles (including the above stated observer pattern) and [b] **Reactive system** where an entire system follows the guidelines of the “[reactive manifesto](http://www.reactivemanifesto.org/)”. The latter one in fact is much bigger picture.

![image](/posts/2020-04-16_going-reactive/images/3.png#layoutTextWidth)
Courtesy: [https://www.lightbend.com/white-papers-and-reports/reactive-programming-versus-reactive-systems](https://www.lightbend.com/white-papers-and-reports/reactive-programming-versus-reactive-systems)

There is a really [cool post](https://www.lightbend.com/white-papers-and-reports/reactive-programming-versus-reactive-systems) about this difference from Lightbend, do check it out! **_We will however stick to the “reactive-programming” for the scope of this article_**.

### Reactive Programming

We just saw that we can implement reactive using our plain-old Observer pattern or a Publisher-Subscriber (PubSub) pattern.
> So, is this it?

Try to fit every piece of your code with a Pub-Sub pattern, you would need certain disciplinary guidelines to be able to make use of it without pulling your hairs out! In fact there are more than just PubSub and Observer pattern to implement reactive e.g., event-loop, actor model etc.

There are some fundamental building block of the reactive programming model:

**_Non-blocking:_** Execution of a task shouldn’t block another task’s execution.
> In our PuSub context, any event should be handled without blocking the execution of upcoming events.

**_Asynchronous:_** Tasks happen asynchronously/separately and may notify after they’re done. Most popular programming pattern seen with this model is callbacks.

CompletableFuture is a very good example for asynchronous programming in Java:

{{< script src="https://gist.github.com/lprakashv/a0a9f913f58b3a64f392b46c88bbe344.js" >}}

The above code is asynchronous as well as it won’t block! Most often than not, **_non-blocking and asynchronous are the same thing_**. If a piece of code is asynchronous, it has to be non-blocking and vice-versa.

There is one major problem with the callbacks, and that is the [**_Callback Hell_**](http://callbackhell.com/) when we have more than 2 nested callbacks, the code starts to look obscure and becomes unmaintainable very quickly.

{{< script src="https://gist.github.com/lprakashv/73cdeb5053ae790f45ac29e7c242b5ed.js" >}}

**_Functional/Declarative:_** To overcome the callback hell and be able to compose (or chain) the operations on the events subscribed, we should use the functional/declarative style. Suppose there is a high level construct of Publisher and Subscriber such that we could use:

{{< script src="https://gist.github.com/lprakashv/e74478507095de99f6b2c26c4e2c20bf.js" >}}

The above code looks more elegant even though it performs a lot of things in steps with a merge chaining of functions. It was just an example taken from Spring Webflux’s Publisher/Subscriber API. There are other reactive libraries and frameworks where this type of functional composition and chaining is possible.

Java 9 also has introduced [Reactive Streams](https://www.reactive-streams.org/) and it would be exciting to see how this evolves over time.

### OK, what to I get from being Reactive?

In a traditional blocking code, a thread may get blocked and awaits for the result of some other task. While waiting, it is simply doing nothing! But since, the thread is there, it will consume the precious CPU cycles, waking up checking if the execution is completed and going back to sleep if the result has not arrived.

![image](/posts/2020-04-16_going-reactive/images/4.png#layoutTextWidth)

While, non-blocking code usually implemented using either,

**_Event-loop_**: I is essentially just a single thread! This event-loop executes/notifies the process to be run/invoked next without getting blocked. Hence, instead of multiple threads waiting for the resource, there’s just this one thread which handles all the I/O and resource allocation to different requests. Just like a waiter does for multiple customers. Example implementations are Vert.x, nodejs, etc.

![image](/posts/2020-04-16_going-reactive/images/5.png#layoutTextWidth)

**_Event driven thread-pool backed mechanism_**: Event driven mechanism involving very small number of threads usually employs some virtual process units (actors, verticles, queue etc.) on top of a thread-pool framework (Fork-Join) making an efficient use of it. Example implementations are Akka Actor model, Reactor, etc.

![image](/posts/2020-04-16_going-reactive/images/6.png#layoutTextWidth)

In addition to that, subscribers being notified (push based) on events by the publisher means that subscribers don’t have to keep polling for the events, saving further more CPU resources.

Ultimately this all leads to better resource management and this is why the reactive model can work with even lesser number threads.

### Why the sudden Need?

We live in the era of “clouds” and “scale”. And by scale, I mean massive scale with thousands to hundreds of thousands users concurrently using your application.

Before the “reactive” hype, every web application out there used to work on a synchronous/blocking **_“1 thread per request model”_**. Which means that **a thread is allocated for every request**! This model served perfectly well for us in past, but in today’s age of mobile apps cheaper and accessible internet, the number of users a “viral” app has to handle can grow really fast.

This massive scale demands resources (larger or more machines) and getting resources in cloud costs money! So, we desperately needed a model which could scale even with lesser resources. In our case lesser number of threads for a highly concurrent application.

### Use cases

As we discussed about this reactive model of programming, you might have had the impression of this being the holy grail for modern web programming. This does in fact also add some noticeable complexity to the system. As they say,
> If you consider all you have is as a hammer, everything else will start looking like a nail!

There is a lot, which is required from a developer to develop truly reactive applications:

**_Discipline is Needed:_** If you are using a reactive framework and the database driver is blocking, you will end up blocking threads, same applies to every other block of you system. Hence, to have a proper reactive application, you have no option but to go **_“all reactive”_**!

{{< figure src="https://media4.giphy.com/media/j3KXqE52HwpQcatFj5/giphy.gif?cid=790b7611301d508f9af34d6b8c45b49360970b1b15d3050a&rid=giphy.gif&ct=g" >}}

This adds even more complexity and does influence many critical design decisions that have to be made, such as:

1. Which DB to use, does it have reactive drivers?
2. Does the libraries I am using support reactive?
3. Is there any blocking operation that I am doing within my system?
4. Do I have written appropriate adapter/wrappers over all the non-reactive components?

## Conclusion

So, better stick to the traditional frameworks unless there is a need otherwise. Some such scenarios could be:

* Highly concurrent application.
* With limited resources.
* Handling request spikes (back-pressure).

This is all from me and hope you got some reactive knowledge out of this post.

Thanks for Reading and have a Good day :)
