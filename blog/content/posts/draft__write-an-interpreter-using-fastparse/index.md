---
title: "Write an Interpreter using “fastparse”!"
author: ""
date: 
lastmod: 2022-08-13T01:15:05+05:30
draft: true
description: ""

subtitle: "I remember when I was  learning programming in my college days, I started writing a math expression calculator with simple expressions like"




---

I remember when I was  learning programming in my college days, I started writing a math expression calculator with simple expressions like
`4 * 4 + 2 / 3`

I then  started all jumpy and I even started thinking of making it more generic for any type of nested expression using parenthesis,
`4 * (2 + (1 + 1) ^ 1) + 2 / (1 + 2)`

Which looks a daunting task when you have  just started learning programming. Then I got even more zealous of adding functions as well…
`square(2) * (sqrt(4) + (1 + 1) ^ cube(1)) + 2 / (1 + 2)`

It is really a tedious job but years laters, I came across a wonderful library called “[fastparse](http://www.lihaoyi.com/fastparse/)” and it just blew me away! Huge thanks to [Li Haoyi](https://twitter.com/li_haoyi) for this.

Now, writing a parser or even a short interpreter for a custom programming language will feel like a breeze.
