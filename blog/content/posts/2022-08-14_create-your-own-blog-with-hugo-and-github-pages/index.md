---
title: "Create Your Own Blog With Hugo and Github Pages"
date: 2022-08-14T16:06:48+05:30

description: ""

subtitle: "In this post we will explore how we can setup our own blog using Hugo, hosted on Github pages using Github Actions for auto deployment"

image: "/posts/2022-08-14_create-your-own-blog-with-hugo-and-github-pages/images/gh-hugo.png"
images:
  - "/posts/2022-08-14_create-your-own-blog-with-hugo-and-github-pages/images/gh-hugo.png"
  - "/posts/2022-08-14_create-your-own-blog-with-hugo-and-github-pages/images/1.png"
  - "/posts/2022-08-14_create-your-own-blog-with-hugo-and-github-pages/images/2.png"
  - "/posts/2022-08-14_create-your-own-blog-with-hugo-and-github-pages/images/3.png"
  - "/posts/2022-08-14_create-your-own-blog-with-hugo-and-github-pages/images/4.png"
  - "/posts/2022-08-14_create-your-own-blog-with-hugo-and-github-pages/images/5.png"
  - "/posts/2022-08-14_create-your-own-blog-with-hugo-and-github-pages/images/6.png"
  - "/posts/2022-08-14_create-your-own-blog-with-hugo-and-github-pages/images/7.png"
  - "/posts/2022-08-14_create-your-own-blog-with-hugo-and-github-pages/images/8.png"

aliases:
    - "/create-your-own-blog-with-hugo-and-github-pages"

tags:
  - hugo
  - blog
  - github pages
  - tutorial
  - website
  - github actions
  - markdown

---

![Image](/posts/2022-08-14_create-your-own-blog-with-hugo-and-github-pages/images/gh-hugo.png#layoutTextWidth)

In this post we will explore how we can setup our own blog using [Hugo](https://gohugo.io/) which claims to be "_The world’s fastest framework for building websites_". And for hosting, we will use [Github pages](https://pages.github.com/) and automatic deployments using [Github Actions](https://github.com/features/actions) workflow.

So let's get started, shall we?

## The Github.io Repository

If you have a [Github.com](github.com) account, you can create your personal static website easily by creating a special repository with name __"\<your-github-user-name\>.github.io"__.

![repo setup](/posts/2022-08-14_create-your-own-blog-with-hugo-and-github-pages/images/1.png#layoutTextWidth)

- By default, you'll be able to see the contents of the README.md file by opening the link __"\<your-github-user-name\>.github.io"__.
- You can place an __index.html__ file along with other static content (css, images, js, etc files) in the repository to render your desired website content.

Elaborate steps to setup your own Github pages website can be found [here](https://pages.github.com/)

__Problem:__ We have found a way to host our static website for free but we need to still create our actual website, which can become quite tedious if you do it from scratch.

To overcome this problem, we can use any of the static site generators available in the market, for example [Jekyll](https://jekyllrb.com/), Hugo, and many more. However, we will limit ourselves to using Hugo and try to build our site using that.

## [Hugo](https://gohugo.io/)

> Hugo is one of the most popular open-source static site generators. With its amazing speed and flexibility, Hugo makes building websites fun again.

### Install and Setup

Install using Homebrew:

```bash
brew install hugo
```

for other methods if installing, please refer [this](https://gohugo.io/getting-started/installing)

Creating a new site (your blog), it's better to create it as a sub-folder inside your github.io repository:

```bash
# clone you github.io repository
git clone https://github.com/<your-user-name>/<your-user-name>.github.io.git

# change directory into the cloned repository folder
cd <your-user-name>.github.io

# now create a blog site sub-folder named "blog" using hugo
hugo new site blog
```

You can then test you website in development mode using:

```bash
cd blog

hugo server -D
```

### Adding Theme

There are lots of pre-built themes for you Hugo site, you can choose from this [hugo themes gallery](https://themes.gohugo.io/).

We will use [archie theme](https://themes.gohugo.io/themes/archie/) for our blog, which looks something like:

![Archie Theme](/posts/2022-08-14_create-your-own-blog-with-hugo-and-github-pages/images/2.png#layoutTextWidth)

```bash
cd blog
git submodule add https://github.com/athul/archie.git themes/ananke
```

Open `blog/config.toml` file in an editor and add the line:

```yml
theme = "archie"
```

### Creating Posts

You can create a post by running the command `hugo new posts/<any-subdirectory-to-be-created>/<name-of-the-post-with-hyphenated-words>.md` in __blog__ folder:

```bash
# make sure you are under hugo site folder
cd blog

hugo new posts/my-first-post.md
```

This will create a markdown file with name __my-first-post.md__ under folder __blog/content/posts__ with contents:

```md
---
title: "My First Post"
date: 2022-08-14T16:06:48+05:30
draft: true
---

```

This is called the __front-matter__ for your post and you can even add more metadata parameters like __tags__, __description__, __subtitle__, __images__ etc. You can refer [this](https://gohugo.io/content-management/front-matter/) for more details.

You can now edit this file and add content in [markdown format](https://www.markdownguide.org/cheat-sheet/).

#### Create posts inside sub-folder

```bash
# make sure you are under hugo site folder
cd blog

hugo new posts/my-first-post/index.md
```

This will create a folder named __my-first-post__ containing __index.md__ file with the same content instead of just one file.

This way we can have other static content like images/videos/gifs in out post folder and we can use those in our __index.md__ file, this ways we can manage separate files for each post.

### Starting Server & Building Deployable Static Content

Running Hugo server to see changes locally

```bash
$ hugo server -D

                   | EN
+------------------+----+
  Pages            | 10
  Paginator pages  |  0
  Non-page files   |  0
  Static files     |  3
  Processed images |  0
  Aliases          |  1
  Sitemaps         |  1
  Cleaned          |  0

Total in 11 ms
Watching for changes in /Users/bep/quickstart/{content,data,layouts,static,themes}
Watching for config changes in /Users/bep/quickstart/config.toml
Environment: "development"
Serving pages from memory
Running in Fast Render Mode. For full rebuilds on change: hugo server --disableFastRender
Web Server is available at http://localhost:1313/ (bind address 127.0.0.1)
Press Ctrl+C to stop
```

Building static content to deploy on any hosting side (github pages in our case)

```bash
hugo -D
```

This will translate our markdown content for our posts into HTML/CSS files in __blog/public__ folder, which can directly be served for our website.

We can also use `hugo --minify` to have the minified static files for production deployment).

## Github Actions

Github Actions workflow provide an out of the box CI/D (continuous integration / continuous deployment) for our code. We can provide the actions to be taken on our code (such as run commands, copy data etc.) based on activities being performed on the repository (branch push, merge etc.).

### Setup Workflow to deploy Github.io site

Click on __Actions__ tab on your repository page

![Click Actions](/posts/2022-08-14_create-your-own-blog-with-hugo-and-github-pages/images/3.png#layoutTextWidth)

Then, navigate __New workflow__ -> __setup a workflow yourself__

![Click Actions](/posts/2022-08-14_create-your-own-blog-with-hugo-and-github-pages/images/4.png#layoutTextWidth)

Here, you can define your workflow in YAML format.

This is the minimal setup to be required for Hugo deployment for deployment of your blog:

```yml
name: blog site github pages publish

# Controls when the workflow will run
on:
  # Triggers the workflow on push or pull request events but only for the "master" branch
  push:
    branches: ["master"]

  # Allows you to run this workflow manually from the Actions tab
  workflow_dispatch:

# A workflow run is made up of one or more jobs that can run sequentially or in parallel
jobs:
  deploy:
    # The type of runner that the job will run on
    runs-on: ubuntu-latest

    # Steps represent a sequence of tasks that will be executed as part of the job
    steps:
      # Checks-out your repository under $GITHUB_WORKSPACE, so your job can access it
      - uses: actions/checkout@v3
        with:
          submodules: true # Fetch Hugo themes (true OR recursive)
          fetch-depth: 0 # Fetch all history for .GitInfo and .Lastmod

      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v2
        with:
          hugo-version: "latest"
          extended: true
      - name: Build
        working-directory: ./blog
        run: hugo --minify

      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./blog/public
```

The above workflow simply defines:

- Workflow is triggered when we push changes in __"master"__ branch
- Runs the job __"deploy"__ when triggered
- deploy has 3 steps:
  - checkout the branch using built-in __actions/checkout@v3__ plugin
  - setup hugo using 3rd party plugin named __peaceiris/actions-hugo@v2__, this installs __hugo__ on the workflow system
  - build by running command `hugo --minify` inside directly __./blog__
  - deploy using 3rd party Github Pages plugin __peaceiris/actions-gh-pages@v3__, with publish directory as __./blog/public__

Once this in place and well understood, click on __Start commit__, then __Commit changes__.

This will create a __main.yml__ with the above content under __.github/workflows__ folder in your repository, you can separately edit that later if required.

The gh-pages plugin used in the workflow actually creates another branch named __gh-pages__ for deployment. So, to use that in our Github.io website we need to switch our deployment branch from __master__ to __gh-pages__.

Click on __Setting__ tab, then click on __pages__ on side bar, then select the branch as gh-pages from Deploy from branch section:

![Click Actions](/posts/2022-08-14_create-your-own-blog-with-hugo-and-github-pages/images/5.png#layoutTextWidth)

Voila, now your blog site up and running! You can now go and open your website using __\<your-github-username\>.github.io__.

### Setup your Custom Domain for Github.io site (optional)

If you already have purchased a domain for yourself, you can definitely use that to point to your blog site. You just need to update your DNS provider's (mine is [GoDaddy.com](godaddy.com)) settings to point to your Github.io website.

Update your DNS records:

- Edit the record with __type "A"__ with value to IP address __185.199.108.153__. This will point your custom domain to GitHub's server over HTTPS.
- Edit the record with __type "CNAME"__ with value as your Github.io website (\<username\>.github.io).
- Add 3 more __type "A"__ records with values having IP addresses __185.199.109.153__, __185.199.110.153__, __185.199.111.153__.

![DNS Type A](/posts/2022-08-14_create-your-own-blog-with-hugo-and-github-pages/images/7.png#layoutTextWidth)

![DNS Type CNAME](/posts/2022-08-14_create-your-own-blog-with-hugo-and-github-pages/images/8.png#layoutTextWidth)

Now, setup your custom domain on you Github pages website.

Click on __Settings__ tab, then click __pages__ on side bar, then enter the Custom domain in the __Custom domain__ section.

![Custom Domain Click Actions](/posts/2022-08-14_create-your-own-blog-with-hugo-and-github-pages/images/6.png#layoutTextWidth)

Now, to update automatic CNAME addition on gh-pages deployment, edit your __Deploy__ (last) step workflow and add cname attirbute:

```yml
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./blog/public
          cname: <your-custom-domain> # <----- add this
```

<!--adsense-inarticle-->

## Conclusion

In this article, we built and deployed our blog site from scratch and for free!

We touched upon various topics:

- Github pages and setting up your own user site
- Hugo static site generator and creating site and adding posts to the site using markdown
- Github Actions workflows and setting up a workflow to deploy your hugo site on each code push
- Setting up your custom domain to point to your Github pages website

_Fin._
