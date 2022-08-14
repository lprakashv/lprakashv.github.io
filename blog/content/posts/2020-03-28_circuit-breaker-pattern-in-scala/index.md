---
title: "Circuit Breaker pattern in Scala"
author: "Lalit Vatsal"
date: 2020-03-28T20:30:28.841Z
lastmod: 2022-08-13T01:14:50+05:30

description: ""

subtitle: "Circuit breaker pattern is a common microservice resiliency pattern to make system responsive after series of failures and have a fallback…"

image: "/posts/2020-03-28_circuit-breaker-pattern-in-scala/images/1.jpeg"
images:
 - "/posts/2020-03-28_circuit-breaker-pattern-in-scala/images/1.jpeg"
 - "/posts/2020-03-28_circuit-breaker-pattern-in-scala/images/2.png"
 - "/posts/2020-03-28_circuit-breaker-pattern-in-scala/images/3.png"


aliases:
    - "/circuit-breaker-pattern-in-scala"
    - "/posts/circuit-breaker-pattern-in-scala"

tags:
  - "scala"
  - "circuit breaker pattern"
  - "microservice patterns"

---

![image](/posts/2020-03-28_circuit-breaker-pattern-in-scala/images/1.jpeg#layoutTextWidth)

[**Circuit breaker pattern**](https://martinfowler.com/bliki/CircuitBreaker.html) is a common microservice resiliency pattern to make system responsive after series of failures and have a fallback mechanism.

[NOTE] Spoiler — This would be a simple implementation and the Scala code would be stateful and have side-effects.

### The Need

Doing a remote call or executing a task which is outside the domain boundary of the system is very common in modern applications. Especially in microservice world, we are bound to make calls to other microservices.

In such scenarios, we need to consider eventual failures. If some failures are too continuous and consistent in nature, they can hog too much of the system resources resulting into failures. We can avoid such cases using the circuit-breaker pattern.

### The Concept

![image](/posts/2020-03-28_circuit-breaker-pattern-in-scala/images/2.png#layoutTextWidth)
courtesy: [https://martinfowler.com/bliki/CircuitBreaker.html](https://martinfowler.com/bliki/CircuitBreaker.html)

The concept is simple, the circuit represents the connection between the caller and the callee. It can only have 3 states: **closed**, **open** and **half-open**. The system starts with the “closed” circuit initially.

We monitor the consecutive (or within a time window) failures from the callee and when the failures exceed a threshold we trip the circuit to “open” and all the further calls from the caller won’t reach the callee and rather caller is returned with a default fallback result.
> — can be implemented using a **failure result counter.**

We also keep monitoring the time since opening the circuit and when a certain timeout is reached, we put the circuit to “half-open” meaning, only one ‘probe’ call will pass through and its result will determine if the circuit will be closed or opened based on its success or failure.
> — can be implemented using a **background timer.**

### Implementation

**CircuitState** — a trait extended by possible states

{{< script src="https://gist.github.com/lprakashv/3b9aceb424a00f7b62289db568e8bdfe.js" >}}

**CircuitResult[T]** — a trait extended by Success and Failure results of the Circuit with success return type T.

{{< script src="https://gist.github.com/lprakashv/9457e7f0670f05bad084f60802789e0d.js" >}}

**Circuit[R]** — a class denoting a circuit where the call returns the result of type Future[R], future denoting an async call.

{{< script src="https://gist.github.com/lprakashv/f91ade5061ab15a70a08ff34065f61e1.js" >}}

States of the Circuit

{{< script src="https://gist.github.com/lprakashv/875480ef20e6e1191fcce3405e7bba90.js" >}}

Transition of states

{{< script src="https://gist.github.com/lprakashv/1e06d37addcca8af52968e33e89dfa86.js" >}}

**Main block execution handler** — It acts as a router and invokes other handlers based on the Circuit’s state. After state transition, the thread request may come back here to be routed again based on the updated state.

{{< script src="https://gist.github.com/lprakashv/5d73aed0e919a43bf6a2e3620e8ddf05.js" >}}

**Handling failure response from the Callee** —

{{< script src="https://gist.github.com/lprakashv/3d55a8db8e545be12459e24ca8cf7942.js" >}}

**Handling closed circuit**— Executing the provided block of code and yield a success or failure as the result asynchronously, while maintaining/updating the count of consecutive failures.

{{< script src="https://gist.github.com/lprakashv/ff0aecba16bf2b41730e56a9f9f205dd.js" >}}

**Handling Half-Open Circuit** —

{{< script src="https://gist.github.com/lprakashv/e83dc09914510936594920693b89a61f.js" >}}

**Handling open circuit**— return the successful future with CircuitSuccess wrapping the default value.

{{< script src="https://gist.github.com/lprakashv/4bf1d46eb8a5ea9a38290c970d86d185.js" >}}

**Half-Opener Background Timer** — Will trip the circuit to half-open after timeout reached since opening the circuit.

{{< script src="https://gist.github.com/lprakashv/fc539d500f17fe3e2f82094a358d4a0f.js" >}}

**CircuitImplicits** — Implicits making the use of our Circuit class a breeze!

{{< script src="https://gist.github.com/lprakashv/1dfe69c3d933da42de263444b7667247.js" >}}

We can now do something like:

```scala
implicit val sampleCircuit: Circuit[Int] = new Circuit[Int](
    "sample-circuit",
    5,                // max allowed consecutive closed failures
    5.seconds,        // half-opener timeout
    1,                // max allowed consecutive half-open failures
    -1,               // invalid success result
    _println
_)

//this will use the above created circuit to execute
Future.successful(2 + 2).executeAsync
```

<!--adsense-inarticle-->

**Testing it out** — You can find the test cases [here](https://github.com/lprakashv/scala-utils/blob/master/src/test/scala/com/lprakashv/resiliency/CircuitTest.scala).

![image](/posts/2020-03-28_circuit-breaker-pattern-in-scala/images/3.png#layoutTextWidth)
