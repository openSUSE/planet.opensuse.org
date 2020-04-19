# 🌎 [Planet openSUSE](planet.opensuse.org)

Planet openSUSE is a web feed aggregator that collects blog posts from people who contribute to openSUSE.

## Switched to new repository

In March 2020, we switched to a new repo and completely new software for planet.opensuse.org. Please see [planet-o-o](https://github.com/openSUSE/planet-o-o) for the new repo.

## Adding your feed

This section describes the workflow for this - now unused - repo and is only kept for historical reasons.
Please see [planet-o-o](https://github.com/openSUSE/planet-o-o) for instructions how to add your feed nowadays.

If you want to get your blog added, we prefer pull requests via github. 

* Fork this repository
* Edit [planetsuse/feeds](https://github.com/openSUSE/planet.opensuse.org/blob/master/planetsuse/feeds) and add:
  * the URL to the RSS/Atom feed of your blog
  * the language of your blog, especially if it's not in English
  * your full name (e.g. John Doe)
  * your IRC nickname on Freenode, if you have any (e.g. jdoe)
  * whether you are an [openSUSE Member](https://en.opensuse.org/openSUSE:Members) so that a "member" button can be placed besides your name on the feedlist
  * a [hackergotchi](https://en.wikipedia.org/wiki/Hackergotchi) -- while it's not mandatory, it is a lot nicer for the readers. If you need help with this send a picture to the openSUSE Artwork team.
* Send a pull request once you are finished

Have a look at [planetsuse/config](https://github.com/openSUSE/planet.opensuse.org/blob/master/planetsuse/config) if you want to know more about possible options. 

An alternative might be an email to admin@opensuse.org - but you would not visit this site if you want to use email, correct? ;-)

