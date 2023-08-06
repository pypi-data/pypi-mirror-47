# lastversion 

[![Build Status](https://travis-ci.org/dvershinin/lastversion.svg?branch=master)](https://travis-ci.org/dvershinin/lastversion)

A tiny command line utility that helps to answer one simple question:

> What is the latest released version for a GitHub project?

GitHub has an API endpoint [here](https://developer.github.com/v3/repos/releases/#get-the-latest-release). But if you're here, then you know how it sucks:

A release would show up in this API response *only* if it was filed formally using GitHub release interface. 
Thus, you can find many (if not most) GitHub projects whose Releases are simply not visible through the API, but only through the actual Releases page.

But we want to get last version on the command line, without looking at Releases page :). Meet `lastversion`.

Its primary use is for build systems - whenever you want to watch specific repositories for released versions in order to build packages automatically.
Or otherwise require getting latest version in your automation scripts.

[Like I do](https://www.getpagespeed.com/redhat)

## Synopsys

    lastversion apache/incubator-pagespeed-ngx #> 1.13.35.2
 
 That repository specifically, is a good example. Because using only API on it will yield an ancient release:
 
     lastversion --nosniff apache/incubator-pagespeed-ngx #> 1.9.32.10
 
 Why is because at some point the maintainers of the repository did a formal UI release, but later used the standard approach.
 
 Sure enough, this can't work in 100% cases, especially if developers did not tag their releases in a sane manner - some don't even provide a version number in their "release tags".
 
 But hey, it works for most repositories and I've added Travis tests for some various repositories.
 
 ## Usage
 
 ```
 usage: lastversion [-h] [--nosniff] [--novalidate] R
 
 Get latest release from GitHub.
 
 positional arguments:
   R             GitHub repository in format owner/name
 
 optional arguments:
   -h, --help    show this help message and exit
   --nosniff
   --novalidate
```

The `--nosniff` will disable the magic and only API will be used (yuck).

The `--novalidate` will disable validation of fetched version.

### Installation for CentOS 7

    yum install https://extras.getpagespeed.com/release-el7-latest.rpm
    yum install python2-lastversion
    
## Installation for other systems

The script requires Python 2.7 and few dependencies. Pip should take of those:

    pip install lastversion

## Tips

If you're planning to fetch versions for a whole lot of projects, setup your GitHub API token in `~/.bashrc` like this:

    export GITHUB_API_TOKEN=xxxxxxxxxxxxxxx

So `lastversion` will use it to get larger API calls allowance from GitHub. Although this is rarely needed, because `lastversion` usually does not resort to API calls because it finds release version through parsing Releases page earlier.