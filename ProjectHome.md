## This project has [moved to GitHub](https://github.com/sampsyo/beets). ##

**Beets** is the media library management system for obsessive-compulsive music geeks.

The purpose of beets is to get your music collection right once and for all. It catalogs your collection, automatically improving its metadata as it goes using the [MusicBrainz](http://musicbrainz.org/) database. It then provides a bouquet of tools for manipulating and accessing your music.

Here's an example of beets' brainy tag corrector doing its thing:

```
$ beet import ~/music/ladytron
Tagging: Ladytron - Witching Hour
(Distance: 0.016165)
 * Last One Standing -> The Last One Standing
 * Beauty -> Beauty*2
 * White Light Generation -> Whitelightgenerator
 * All the Way -> All the Way...
```

Because beets is designed as a library, it can do almost anything you can imagine for your music collection. Via [plugins](http://readthedocs.org/docs/beets/-/plugins/index.html), beets becomes a panacea:

  * Embed and extract album art from files' metadata.
  * Listen to your library with a music player that speaks the [MPD](http://mpd.wikia.com/) protocol and works with [a staggering variety of interfaces](http://mpd.wikia.com/wiki/Clients).
  * Fetch lyrics for all your songs from databases on the Web.
  * Manage your [MusicBrainz music collection](http://musicbrainz.org/show/collection/).
  * Analyze music files' metadata from the command line.

If beets doesn't do what you want yet, [writing your own plugin](http://readthedocs.org/docs/beets/-/plugins/index.html#writing-plugins) is shockingly simple if you know a little Python.

Install beets with `pip install beets` or by [downloading the package](http://code.google.com/p/beets/downloads/list). You might then want to read the [Getting Started guide](GettingStarted.md). Then follow [@b33ts](http://twitter.com/b33ts) on Twitter for updates.

<wiki:gadget border="0" url="http://stefansundin.com/stuff/flattr/google-project-hosting.xml" width="55" height="62" up\_url="http://beets.radbox.org/" />