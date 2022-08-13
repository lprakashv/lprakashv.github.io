---
title: "Life with Microservices"
author: ""
date: 
lastmod: 2022-08-13T01:15:05+05:30
draft: true
description: ""

subtitle: "Here is a hypothetical but typical evolution of a simple application service over time."




---

_Here is a hypothetical but typical evolution of a simple application service over time._

We start with a simple service doing simple things. Each and every internal part works perfectly and in-synergy!
> Life is very good!

Then we see some load growing and we start to distribute our service with multiple instances, to handle all the incoming load. With a little plumbing we are up again to handle distributed load. Yeah, we have occasional pains while deploying and fixing but life still seems good till we keep limited and planned rollouts.

Our service application starts to grow even bigger as we keep adding more and more features to it as a result number of components grow. Now, as we are doing everything under the sun,
> Life gets a little messier 

Each of these components becomes more and more feature rich hence, that requires and entire team to handle it. Each team’s even smallest feature now starts impacting our deployments and and other teams’ release. They now start asking for a separate service for them to be able to grow and develop faster. 
> Life starts becoming hectic!

Now, we start breaking our application apart to hand each component to their respective teams. As we burn our midnight oil all in hope to have comfortable mornings ahead.
> Life becomes a little sleepless

We now have all the teams happy with their microservices and life goes normal again. Only problem is that every issues faced is somehow blamed to-fro between teams and ultimately infra has to take it. With typical arguments being,
> Our service didn’t receive requests.> Message queue / Kafka went down.> Your service keeps bombarding our services unnecessarily.> We expected your service to do this/that…> Life gets complicated

We now keep growing bigger. Some of the microservice start handling more and more load. We now have a reputation to protect and customers to serve. We get even more aspirational and try to improve latency and quality. We start running more and more instances of some microservices and move to auto-scalable, multi-region cloud services. We have now opened a pandora-box of problems for us:

If there is one truth in cloud services and that is: **“Failure is Inevitable”**!

Failures can be:

1.  Hardware failure
2.  Software failure
3.  Network failure

We have explosion of failure possibilities now! 
> Why?

Because, we have: 

1.  more hardware —  auto-scalable cloud VMs.
2.  more software — multiple application instances of multiple microservices using multiple infrastructures tools.
3.  more network — multi-cloud, multi-region services talking over network to one another.

This leads to:

*   Service reliability becomes really critical.
*   Need to handle failures which can and will cascade to other services.
*   Configurations managements and keeping all instance’s configs in sync seems daunting.
*   Multiple load balancers needed.
*   Reliance on Infrastructure increases and we start thinking of going for managed infra services like cloud managed databases, async queues, load balancers etc.
*   Deploying in such scenarios becomes painful and investment into containers, continuous integration and continuous deployment seems worth it.

We start building a DevOps infrastructure and need a strong DevOps team.
> Life Becomes Challenging

We keep trying to solve our problems and challenges life has thrown to us. We now get pretty confident and look back to our journey full of learnings.
> Life seem Enjoyed!

If you look at this journey you can see how much effort and learning is needed to go fully into microservice environment, which demands investment both in time and resources. We have to analyse if this is worth all the other benefits. 

My learnings and experiences working in the microservice environment,

*   DevOps plays one of the very important role.
*   Have a good CI/CD pipeline to work efficiently.
*   Have fail-overs and setup disaster-recovery strategies for each infrastructure component e.g., database, kafka, cache etc.
*   Adopt frameworks and libraries built for cloud-native applications e.g., Spring Cloud, Netflix OSS, resilience4j, Akka etc.
*   Invest on monitoring tools Lenses, Grafana, Prometheus, Hystrix, Turbine etc.
*   Setup alerting system for various metrics and activities such as build-failures, VM replace, application failures, key metric drops etc.

Hope this helps. Thank you for reading :)
