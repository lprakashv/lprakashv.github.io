---
title: "Intro to Reactive Spring"
author: ""
date:
lastmod: 2022-08-13T01:15:04+05:30
draft: true
description: ""

subtitle: "TODO — 1. flux and mono examples (initialisations, simple operations, chaining, error handling, when to subscribe), 2. functional endpoints…"

image: "/posts/draft__intro-to-reactive-spring/images/1.png"
images:
 - "/posts/draft__intro-to-reactive-spring/images/1.png"
 - "/posts/draft__intro-to-reactive-spring/images/2.png"
 - "/posts/draft__intro-to-reactive-spring/images/3.png"
 - "/posts/draft__intro-to-reactive-spring/images/4.gif"


---

TODO — 1. flux and mono examples (initialisations, simple operations, chaining, error handling, when to subscribe), 2. functional endpoints example.

![image](/posts/draft__intro-to-reactive-spring/images/1.png#layoutTextWidth)


### Spring 5

Spring 5 web stack comes in 2 different flavours, Spring MVC and Spring WebFlux. Spring MVC is your regular old Spring’s web framework while Spring WebFlux is the reactive counterpart for the Spring MVC.

### Spring Webflux under the hood

Spring WebFlux can be considered a redesign of Spring MVC without taking away its simplicity and modifying the API too much. The following are the key differences with Spring MVC are:

1.  **_Reactive streams:_** Spring Webflux provides complete back-pressure support across all the libraries by utilizing reactive streams implementations provided by “[Project Reactor](https://projectreactor.io/)”.
2.  **_Asynchronous and Non blocking API:_** Spring Webflux provides fully non-blocking APIs. For non-blocking HTTP requests and responses, Java Servlets API has to provide non-blocking support as well, which was included in version 3.1. Hence, Spring Weblux can run on any servlet container using Servlet API 3.1+.
3.  **_Concurrency:_** Based on event loop concurrency model which allows concurrent connections with fewer threads instead on thread per request in Spring MVC.

### Keeping Spring, Spring!

Let’s see an example in action with writing a plain controller with get API:

![image](/posts/draft__intro-to-reactive-spring/images/2.png#layoutTextWidth)


Notice this looks almost same as a Spring MVC controller, the only difference is being the return type “Mono” and “Flux”. This similar experience is what makes the transition to the Spring Webflux really easy.

*   Just like above all the other Spring’s familiar annotations will also work in Webflux.
*   However, there is one differences in the above example, like a reactive repository which should return the reactive data types (Flux and Mono).

### What’s Different?

Following image summarises the difference between stacks of **_Spring MVC_** and **_Spring WebFlux_**.

![image](/posts/draft__intro-to-reactive-spring/images/3.png#layoutTextWidth)
Courtesy: docs.spring.io



There are some notable differences in which are key to understand before starting to build something using Weblux.

**_Flux and Mono:_** Since, the reactive support is enabled using reactive streams implementation provided by the Project Reactor. It uses Reactor’s data types, Flux and Mono to represent typed sequences.

*   Mono — data type to represent a nullable single value, or a stream sequence with 0 or 1 elements.
*   Flux — data type to represent a sequence of values.

Both of the above provide a whole range of features and methods to work with, pretty standard transformation methods being the .flatMap() and .map().

**NOTE:** There is one Gotcha though, Flux/Mono chained expressions only define a process and do not trigger it! We need to call a .subscribe() method start the process/stream.

However, in most of the cases, we do not need to call the .subscribe(), Spring itself does it on receiving requests. We just define multiple processes (Fluxes and Monos) in our services/daos and they eventually are triggered by a controller endpoint which internally manages the subscriptions for requests.

**_Server Sent Events:_** Webflux provides support for the Server sent events with `org.springframework.codec.ServerSentEvent`. And using this is as easy as making a GET endpoint with return type **Flux<ServerSentEvent>**.

Let’s build a demo endpoint for prime numbers as Server sent events with 1 second duration:




Testing it out:

![image](/posts/draft__intro-to-reactive-spring/images/4.gif#layoutTextWidth)


**_A Reactive WebClient:_** There is an out-of-the-box web client shipped with the Spring Webflux to make “reactive” http calls.

**_Functional Endpoints:_** If we ever happen to move away or get bored of creating endpoints using annotations, we can use the functional endpoints. These are almost like the endpoints in many other web frameworks like express, http4s, akka-http, http4k etc.

### It’s Reactive all the way!

Spring Webflux is completely reactive enabling us to write fully reactive applications. Every component of the framework uses its reactive counterpart APIs:

*   Reactive Spring Security
*   Reactive Spring Data
*   Non-blocking server (e.g., Netty)

### Limitations

One major downside of being completely reactive is not-being able to use non-reactive/blocking libraries efficiently. Even though we can still use them by wrapping everything up inside the first-class citizens, Monos and Fluxes. Doing so, the application won’t remain truly reactive and there will be some blocking components in the application.

One major limitation from the standard and official support standpoint is the reactive JDBC support for some of the database drivers. The only database having reactive Spring Data access are:

1.  MongoDB
2.  Cassandra
3.  Couchbase
4.  Redis

We can’t help but notice that all of them are non-relational databases. However, the reactive Spring Data support is not a matter of database supporting reactive but of a reactive driver being available for the database.

Update: There exists an **_R2DBC_** (“Reactive Relational Data Base Connectivity”) library which provides reactive non-blocking API support for some of the mainstream databases like:

*   MS SQL server
*   MySQL
*   PostgreSQL
*   H2

### TL;DR

Spring Framework being most popular and adopted frameworks in Java development community has also embraced the reactive phenomena. The APIs and usage remains fairly similar to Spring MVC framework with additional reactive semantics to ease the developer transition.
