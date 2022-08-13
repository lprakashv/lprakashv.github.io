---
title: "Bulk RDBMS Upserts with Spring"
author: "Lalit Vatsal"
date: 2020-08-28T21:08:07.539Z
lastmod: 2022-08-13T01:14:56+05:30

description: ""

subtitle: "Upserts"

image: "/posts/2020-08-28_bulk-rdbms-upserts-with-spring/images/1.jpeg"
images:
 - "/posts/2020-08-28_bulk-rdbms-upserts-with-spring/images/1.jpeg"
 - "/posts/2020-08-28_bulk-rdbms-upserts-with-spring/images/2.png"
 - "/posts/2020-08-28_bulk-rdbms-upserts-with-spring/images/3.png"
 - "/posts/2020-08-28_bulk-rdbms-upserts-with-spring/images/4.png"
 - "/posts/2020-08-28_bulk-rdbms-upserts-with-spring/images/5.png"
 - "/posts/2020-08-28_bulk-rdbms-upserts-with-spring/images/6.png"
 - "/posts/2020-08-28_bulk-rdbms-upserts-with-spring/images/7.png"
 - "/posts/2020-08-28_bulk-rdbms-upserts-with-spring/images/8.png"
 - "/posts/2020-08-28_bulk-rdbms-upserts-with-spring/images/9.png"
 - "/posts/2020-08-28_bulk-rdbms-upserts-with-spring/images/10.png"
 - "/posts/2020-08-28_bulk-rdbms-upserts-with-spring/images/11.png"
 - "/posts/2020-08-28_bulk-rdbms-upserts-with-spring/images/12.png"
 - "/posts/2020-08-28_bulk-rdbms-upserts-with-spring/images/13.png"
 - "/posts/2020-08-28_bulk-rdbms-upserts-with-spring/images/14.png"
 - "/posts/2020-08-28_bulk-rdbms-upserts-with-spring/images/15.png"
 - "/posts/2020-08-28_bulk-rdbms-upserts-with-spring/images/16.png"
 - "/posts/2020-08-28_bulk-rdbms-upserts-with-spring/images/17.png"
 - "/posts/2020-08-28_bulk-rdbms-upserts-with-spring/images/18.png"
 - "/posts/2020-08-28_bulk-rdbms-upserts-with-spring/images/19.png"


aliases:
    - "/bulk-rdbms-upserts-with-spring-506edc9cea19"

tags:
  - "java"
  - "spring boot"
  - "java 8"
  - "java streams"
  - "ms sql server"
  - "spring data"
  - "apache kafka"
  - "SQL"
  - "database stored procedures"
  - "data ingestion"
  - "data processing"
  - "data pipelines"

---

![image](/posts/2020-08-28_bulk-rdbms-upserts-with-spring/images/1.jpeg#layoutTextWidth)

Upsert is a fairly common terminology in databases, meaning **_Up_**date if the record exists or In**_sert_** the new record. Upserts make more sense in case of simple object save requests with new information.

### Why Bulk?

If we talk about any **_data sync_**, **_data migration_** or **_bulk data update jobs_**, we are bound to have a bulk upsert scenario to update whatever we have in the database and insert all the new rows.

### Solutions

We will be discussing about the solutions present in the Spring Boot environment and inferences we make out of them.

For the testing, I will be using MS SQL Server as the database and will be limited to it’s functionality but the concepts are fairly generalisable.

#### #1 Standard `saveAll()` Solution using Spring JPA

Consider we have a `price` table with a composite unique key/constraints having like with structure:

![image](/posts/2020-08-28_bulk-rdbms-upserts-with-spring/images/2.png#layoutTextWidth)

Then, our entity’s composite primary key and entity classes would look like:

![image](/posts/2020-08-28_bulk-rdbms-upserts-with-spring/images/3.png#layoutTextWidth)

Assume we are consuming a stream of record batches to upsert. To mock this, we have a supplier to generate a random `Price1` object batches of size 1000. The ingestion code:

![image](/posts/2020-08-28_bulk-rdbms-upserts-with-spring/images/4.png#layoutTextWidth)

Let’s see the results:

![image](/posts/2020-08-28_bulk-rdbms-upserts-with-spring/images/5.png#layoutTextWidth)

Now, on looking closely the time taken to persist each batch increases as the table get filled up! What is this?

The culprit is the the method `.save()` of `SimpleJPARepository` class:

![image](/posts/2020-08-28_bulk-rdbms-upserts-with-spring/images/6.png#layoutTextWidth)

Since, the save performs both the insert and update operation, it has to check whether an entity is “new” or not. For which, it has to either check in the persistence context or query the database, which will get complex in time as the table get filled up.

#### #2 Optimisations for Bulk save

Our bottleneck in the previous approach was continuous reads from the DB for a primary key combination to check whether to perform `.persist()` / insert or `.merge()` / update.

To avoid additional querying on the table for `.isNew()` we could have another auto generated unique field (row) which is independent of the business logic. So that, every new object will have a unique id and will always do `.persist()` for them.

Let’s do the modifications on a completely new table (keeping the business columns as they are), with an additional auto-incremented “identity” column :

![image](/posts/2020-08-28_bulk-rdbms-upserts-with-spring/images/7.png#layoutTextWidth)

Here is our entity:

![image](/posts/2020-08-28_bulk-rdbms-upserts-with-spring/images/8.png#layoutTextWidth)

Testing out similar ingestion code will yield the result like below:

![image](/posts/2020-08-28_bulk-rdbms-upserts-with-spring/images/9.png#layoutTextWidth)

Hooray, Constant time and faster inserts! But wait,

![image](/posts/2020-08-28_bulk-rdbms-upserts-with-spring/images/10.png#layoutTextWidth)

There are now duplicate rows with `upc, store_id` combinations

![image](/posts/2020-08-28_bulk-rdbms-upserts-with-spring/images/11.png#layoutTextWidth)

Which is understandable, as we are doing no updates.

#### #3 Plain inserts then merge

The above 2 experiments have encouraged us to keep the insert model for faster inserts and somehow merge (do updates) later.

To achieve this, we can have a “stage” table having a unique auto-generated id for inserts, separate from our target main table. And a pos-ingestion job for merging the records after de-duplicating.

![image](/posts/2020-08-28_bulk-rdbms-upserts-with-spring/images/12.png#layoutTextWidth)

Plain inserts can go as the done above, we will now try to write a “merge” step. This step can very well be database stored procedure due to following reasons:

1. To avoid movement of data and process the bulk data where it resides.
2. Database specific optimisations are built-in.

Following is an example naive implementation of a merge stored procedure for MS SQL, similar merge query features are present most of the mainstream databases.

![image](/posts/2020-08-28_bulk-rdbms-upserts-with-spring/images/13.png#layoutTextWidth)

Executing this took less than a second!

![image](/posts/2020-08-28_bulk-rdbms-upserts-with-spring/images/14.png#layoutTextWidth)

**Important Notes:** The above stored procedure implementation is a very naive approach just to demonstrate and misses on a lot of the aspects to be taken care of in a production environment, like:

* Over utilising transaction log size due to huge data in the merge statement, **_batch-wise merging with id range_**could be implemented here.
* Monitoring and logging procedure failures, a TRY-CATCH based procedure with logging failures in a **_procedure-audit logging table_** could be used.
* A successfully merged batch-range delete instead of truncating the stage table.

#### #Extra: Further Improving batch inserts

If we try to log the hibernate generated SQL statements for our `.saveAll()` operation, we will get something like this:

![image](/posts/2020-08-28_bulk-rdbms-upserts-with-spring/images/15.png#layoutTextWidth)

Here, we are firing single insert statements with values to insert, each going over the network.

There are some improvements that can be done here:

1. Batch the queries and fire in call to the database over network.
2. Rewrite the single queries into a form of single multi-row query.

For first, we can make use of hibernate properties:

```properties
spring.jpa.properties.hibernate.jdbc.batch_size=1000
spring.jpa.properties.hibernate.order_inserts=true
```

For second, there are bulk (multi-row) insert query options available in most of the mainstream database solutions (Postgres, MySQL, Oracle). With syntax like:

```sql
insert into myschema.my_table (col1, col2, col3)
values
(val11, val12, val13),
(val21, val22, val23),
....
(valn1, valn2, valn3);
```

While, Postgres and MySQL do support this features with the help of JDBC flag: **_reWriteBatchedInserts=true_**

But unfortunately, according to [this resource](https://docs.microsoft.com/en-us/sql/connect/jdbc/use-bulk-copy-api-batch-insert-operation?view=sql-server-ver15), ms-sql JDBC driver does not support the multi-row rewrite of the queries. So, if we want to do this, we would have to write the insert queries manually.

Manual insert query creation could look like:

![image](/posts/2020-08-28_bulk-rdbms-upserts-with-spring/images/16.png#layoutTextWidth)

The ingestion code would use `entityManager.createNativeQuery()` method:

![image](/posts/2020-08-28_bulk-rdbms-upserts-with-spring/images/17.png#layoutTextWidth)

Let’s test it out:

![image](/posts/2020-08-28_bulk-rdbms-upserts-with-spring/images/18.png#layoutTextWidth)

Wow!! Those batches of 1000 records took less than a second, let’s look at the milli seconds now:

![image](/posts/2020-08-28_bulk-rdbms-upserts-with-spring/images/19.png#layoutTextWidth)

<!--adsense-inarticle-->

## Conclusion

We can safely infer from our above experiments that:

1. Achieving bulk Upserts are really complicated in relational databases.
2. Spring JPA and Hibernate provided out-of-the-box save methods won’t scale for huge loads.
3. A decoupled (from business columns/fields) independent primary key will help improve the insert performance of the inserts, but will eventually insert duplicate records.
4. Separating insert-only and read (actual) table can be used to improve ingestion performance.
5. A post insert, merge strategy can be used for de-duplicating inserted records. Stored procedures work well in this scenario.
6. Native SQL queries will give the most performant result, use solutions which are as close to the database as possible where performance is critical.

### Testing Environment

* Macbook Pro 2016 model 15" with 16 GB RAM.
* Application uses Java 1.8 with Spring Boot 2.3.3.
* MS SQL server 2017 database in a Docker container.

Thanks for Reading :)
