---
title: "Akka Streams in Java Spring Boot!"
author: "Lalit Vatsal"
date: 2020-04-12T10:45:58.338Z
lastmod: 2022-08-13T01:14:53+05:30

description: ""

subtitle: "Streaming data from a Source to Sink is a very trivial task in today’s data processing and data pipelining systems. Ergo, there are many…"

image: "/posts/2020-04-12_akka-streams-in-java-spring-boot/images/1.png"
images:
 - "/posts/2020-04-12_akka-streams-in-java-spring-boot/images/1.png"
 - "/posts/2020-04-12_akka-streams-in-java-spring-boot/images/2.png"
 - "/posts/2020-04-12_akka-streams-in-java-spring-boot/images/3.png"


aliases:
    - "/akka-streams-in-java-spring-boot"
    - "/posts/akka-streams-in-java-spring-boot"

tags:
  - "java"
  - "akka streams"
  - "spring boot"
  - "data pipeline"
  - "data ingestion"
  - "apache kafka"

---

![image](/posts/2020-04-12_akka-streams-in-java-spring-boot/images/1.png#layoutTextWidth)

Streaming data from a Source to Sink is a very trivial task in today’s data processing and data pipelining systems. Ergo, there are many streaming solutions out there like: Kafka Stream, Spark Streaming, Apache Flink etc.

All of them in one way or another either need an infrastructure to be setup to be able to fully take advantage of them (e.g., HDFS, Spark cluster, Kafka streaming setup etc.) or we need some kind of orchestration among the streaming jobs (e.g., Apache Airflow).

### Akka Streams

Akka streams stands out in this battle and have this advantage of being totally application driven. Akka stream is build on top of the Akka’s celebrated Actor model (which in fact is inspired from Erlang’s actor model). Hence, Akka streams can leverage its battle tested [resiliency, elastic, event-driven and responsive](https://www.lightbend.com/blog/why-do-we-need-a-reactive-manifesto) (see [reactive manifesto](https://www.reactivemanifesto.org/)) capabilities.

**Problems with Akka:**

1. Java developer community has been staying away from the “made-for and built-on scala” Akka platform.
2. Not much documentation and support for the most popular Java framework, “Spring”.

I’m here to tell you otherwise! Inspite of lack of resources available on the internet, we can in-fact do akka-streams in Java and do it with ease.

In this post we will build an Akka stream application **in Java** and with **Spring Boot!** And we will analyse the out of the box benefits we can get using Akka streams. So, let’s ge started…

### Problem Statement

We need a simple realtime stream which consumes all the updates published on a Kafka topic and persists the events in a SQL server database after parsing. And we only want to commit the Kafka offset after the record has been inserted into the database.

![image](/posts/2020-04-12_akka-streams-in-java-spring-boot/images/2.png#layoutTextWidth)
**Lets start a fresh Spring boot project from Spring Initialzr.**

[Spring Initializr](https://start.spring.io/)

We will make the project organised like the tree below which is a pretty standard maven directory structure (since we have chosen to use maven here). You could go with gradle also if you like.

```txt
.
├── pom.xml
└── src
    ├── main
    │   ├── java
    │   │   └── com
    │   │       └── lprakashv
    │   │           └── springalpakka
    │   │               ├── SpringCommandLineApplication.java
    │   │               ├── configs
    │   │               │   ├── AkkaConfig.java
    │   │               │   └── StreamConfig.java
    │   │               ├── dtos
    │   │               │   └── Event.java
    │   │               ├── services
    │   │               │   └── StreamService.java
    │   │               └── utils
    │   │                   └── StreamUtils.java
    │   └── resources
    │       ├── application.yml
    │       └── stream.conf
    └── test
        └── java
            └── com
                └── lprakashv
                    └── springalpakka
```

Don’t bother about the code files in the tree, we will shortly talk about those.

**Add all the required dependencies:**

![image](/posts/2020-04-12_akka-streams-in-java-spring-boot/images/3.png#layoutTextWidth)

**Setup Foundational Akka configurations:**

{{< gist lprakashv 0928b8c9628407ad6d7f5a0d9a76a165 >}}

In every Akka/Akka-Stream application the very basic components needed are the Akka’s **ActorSystem** and **Materializer**. These are needed for a lot of things in this eco-system like, spawning actors, creating stream components, running streams, materializing streams etc.

In the above code, we made sure:

1. We have only one instance beans of both ActorSystem and Materializer throughout our application.
2. Will be instantiated only if **_akka.stream.javadsl.Source_** is in scope.

**Our Kafka Event DTO to consume:**

{{< gist lprakashv 94d2a2eddb36b429ed9a9de4bb36b43c >}}

**Let’s write our Source (Kafka)**: We would like to commit the offsets later hence using a [committableSource](https://doc.akka.io/api/alpakka-kafka/2.0.2/akka/kafka/scaladsl/Consumer$.html#plainSource[K,V]%28settings:akka.kafka.ConsumerSettings[K,V],subscription:akka.kafka.Subscription%29:akka.stream.scaladsl.Source[org.apache.kafka.clients.consumer.ConsumerRecord[K,V],akka.kafka.scaladsl.Consumer.Control]). We will create a Bean out of our committable source to be autowired in our service classes.

{{< gist lprakashv cc7ad527353aad10ea8c0bdc5c4d0a98 >}}

**Now let’s write our Flow (Slick):** We could have cerated a Sink if we were to not bother about persist result and commit Kafka offset anyway (using a “[plainSource](https://doc.akka.io/api/alpakka-kafka/2.0.2/akka/kafka/scaladsl/Consumer$.html#plainSource[K,V]%28settings:akka.kafka.ConsumerSettings[K,V],subscription:akka.kafka.Subscription%29:akka.stream.scaladsl.Source[org.apache.kafka.clients.consumer.ConsumerRecord[K,V],akka.kafka.scaladsl.Consumer.Control])”). We are using flow instead of sink because we want to propagate the committable-offset even after the database stage. We will add the following code in our same config class.

{{< gist lprakashv 865822e16f46cb3cd6274a832a3e9f6f >}}

You might be wondering what is in the **_stream.conf_** file and where did that **_committableMesssageToDTO_** and **_insertEventQuery_** came from?

Slick needs a configuration to create a session which will execute all our DB queries. This config needs to follow the below structure in a **_.conf_** file (which is the standard way to access configs in the typesafe/lightbend world).

```config
event-sqlserver {
  profile = "slick.jdbc.SQLServerProfile$"
  db {
    dataSourceClass = "slick.jdbc.DriverDataSource"
    properties {
      driver = "com.microsoft.sqlserver.jdbc.SQLServerDriver"
      url = "your-db-url!"
      user = "your-db-user!"
      password = "your-db-pass"
    }
  }
}
```

While, the **_committableMesssageToDTO_** and **_insertEventQuery_** are functions which will convert our CommittableMessage to DTO (our record class) and then to SQL insert query.

We can write a Utils class with static functions to generate the SQL like:

{{< gist lprakashv 3a60d3145df7fa49c1ea0480a3f6cf4d >}}

**Now, let’s piece them together and build a stream:**

{{< gist lprakashv 91808cad95f56de6099b5d3d7525a795 >}}

This is it! We can now invoke the startKafkaToDatabaseStream() method from anywhere and it will do our job.

There were a lot of highlighting features there in a single “terse” chain! Let me explain each:

1. **_.buffer(size, overflowStrategy)_**: This will add a fixed-**_size_** buffer into our “flow” which will protect the downstream system from a faster upstream source. We can use the strategies for discarding the messages if the size is full: **_backpressure_** — will down the consumption, **_drophead/droptail/dropbuffer_** — will drop the messages and won’t backpressure and **_fail_** — fails the stream on buffer full.
2. **_.idleTimeout(duration)_**: It will throw a **_java.util.concurrent.TimeoutException_** on idle timeout duration which can be handled using recover/recoverWith.
3. **_.recoverWith(ThrowableClass, fallbackSourceConsumer)_**: Whenever a ThrowableClass.class exception is intercepted, the original source is replaced by a Source received from the fallbackSourceConsumer.
4. **_.throttle(elements, per, maximumburst, mode)_**: Sends elements downstream with a speed limited to (**_elements/per_**), mode=Shaping — makes pauses before emitting to meet the throttle rate, mode=Enforcing — fails with exception when upstream is faster than the throttle rate.
5. **_.mapAsync(parallelism, () -< CompletionStage(value))_**: To process the stage in asynchronous mode with parallelism defined.
6. **_CommitterSettings.create(actorSystem)_**: Creates a default committer settings.

The DrainingControl can be used as:

{{< gist lprakashv 91808cad95f56de6099b5d3d7525a795 >}}

There are a lot of other features of akka stream which were not in scope of this post but still worth to explore. Please checkout [**akka-stream**](https://doc.akka.io/docs/akka/current/stream/index.html) and [**alpakka’s**](https://doc.akka.io/docs/alpakka/current/index.html) documentations.

## Conclusion

We saw that we could easily integrate Akka streams into our Spring Boot projects and leverage Spring’s dependency injection to manage our Akka/Stream beans easily.

There are a lot of streaming features like back-pressure and throttling to name a few which would easily take up a lot of developer hours and brains. And yet, we would have missed some corner cases if not tested thoroughly. Those things we got out-of-the-box in akka-stream’s toolkit.

All in all, Akka-streams along with Alpakka are great tools to have in a data platform stack.

Thanks for reading!
