# lprakashv.com

This repository is the root of [my personal website](https://www.lprakashv.com/). It contains my blog, where I write about software engineering and the technologies I work with.

## Blog

The blog includes posts on observability, Java, Spring, Scala, design patterns, and reactive systems. Visit the [post archive](https://www.lprakashv.com/posts/), browse by [tag](https://www.lprakashv.com/tags/), or read [about me](https://www.lprakashv.com/about/).

## Apps

My website also includes apps at paths such as `www.lprakashv.com/<app-name>`.

<!-- apps:start -->

### [codenames-game](https://www.lprakashv.com/codenames-game/)

An offline (for now) "Codenames Game" app built using Clojurescript and re-frame.

[Repository](https://github.com/lprakashv/codenames-game)

![codenames-game app preview](https://raw.githubusercontent.com/lprakashv/codenames-game/main/demo/Screenshot_2021-02-17_reframe_codenames_1.png)

### [designed-to-scale](https://www.lprakashv.com/designed-to-scale/)

Clone of Designed to Scale - System Design Concepts and Practice

[Repository](https://github.com/lprakashv/designed-to-scale)

![designed-to-scale app preview](https://raw.githubusercontent.com/lprakashv/designed-to-scale/main/showcase/request-lifecycle.jpg)

### [dsa-blueprint](https://www.lprakashv.com/dsa-blueprint/)

DSA Blueprint - Understand coding problem patterns

[Repository](https://github.com/lprakashv/dsa-blueprint)

![dsa-blueprint app preview](https://raw.githubusercontent.com/lprakashv/dsa-blueprint/main/docs/images/learn.jpg)

### [notes](https://www.lprakashv.com/notes/)

Learning Notes

[Repository](https://github.com/lprakashv/notes)

### [patternmatcher4j](https://www.lprakashv.com/patternmatcher4j/)

An FP style pattern matcher library for Java

[Repository](https://github.com/lprakashv/patternmatcher4j)

<!-- apps:end -->

## Site maintenance

The nightly workflow refreshes the app list from public repositories that have GitHub Pages enabled and link to an app path on this domain in their homepage or README. It also follows a repository's GitHub Pages project URL when it redirects to this domain. It uses the repository description and the first suitable image in its README, if available. Repositories without a matching link are skipped; add the app URL and a demo image to their README to include them. Run the workflow manually from the Actions tab to refresh the list sooner.

The workflow builds the blog with Hugo 0.170.1 extended. Update the pinned version after checking the build with the new release.

### Website analytics

The Hugo site uses Google Analytics 4 (GA4). The Pages workflow reads the Measurement ID from the repository Actions variable `GOOGLE_TAG_ID` and passes it to Hugo at build time. Set this variable to the ID for your web stream. It starts with `G-`.

#### Set up or check Google Analytics

1. Sign in at [Google Analytics](https://analytics.google.com/).
2. Open **Admin → Data streams**. Create or select a **Web** stream for `https://www.lprakashv.com`.
3. Copy the stream's **Measurement ID**. It starts with `G-`.
4. In the repository, open **Settings → Secrets and variables → Actions → Variables** and add `GOOGLE_TAG_ID` with that value.
5. Deploy the site. A push to `master` runs the GitHub Pages workflow.
6. Visit the live site, then check the property's **Realtime** report. Data can take up to 30 minutes to appear.

The page tag already sends page views. In the web stream settings, choose whether to enable **Enhanced measurement** for other events, such as scrolls and outbound clicks. Do not add a second GA tag through another plugin or Tag Manager, as that can count visits twice.

See Google's [GA4 setup guide](https://support.google.com/analytics/answer/14183469) for the current account and stream steps.

### About page

The About page renders `blog/content/about/profile-readme.md` as local site content. On pushes to `master`, nightly, and on manual runs, GitHub Actions copies the README and its images from the public `lprakashv/lprakashv` profile repository, commits changes, then builds and deploys the site. Run the workflow manually from the Actions tab to sync it sooner. The sync expects the banner at the repository root and images in its `images` directory.
