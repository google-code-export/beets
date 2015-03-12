This page is for brainstorming ideas that should make into beets after the core functionality is basically working. When will we get around to any of it? Nobody knows!

# Ideas #

## General ##

  * distributedness (play music elsewhere, store a subset of music, edit tags elsewhere...)
  * more extensible (multiple-file) artwork handling
  * convert from iTunes
  * playlists
  * query strings
    * "quoted phrases"
    * -exclusion (i.e., NotQuery)
  * more robust destination filename production
    * deal with duplicates (iTunes' solution: append a serial number to uniquify)
  * tag-based organizing of music (with tags fetched from last.fm)
  * data collection during imports to help optimize thresholds and such
  * major refactoring of importer workflow to be UI-agnostic

## Interfaces ##

  * iTunes library exporter? If you remove the binary database file, it will be regenerated from the XML file ([iTunes module](http://www.math.columbia.edu/~bayer/Python/iTunes/index.html))
  * Library Cleaner GUI (add & fix bad tags)
  * back-end plugin for media players (Banshee, for instance)?
  * a Web interface (with a well-defined REST/JSON API)

## Little utilities ##

  * crap checker: report <=128kbps MP3s, releases ripped by different encoders...
  * new release finder: what else is available by artists I already have some of? ([pylbum](http://code.google.com/p/pylbum/source/browse/) has a similar idea)
  * also which albums are not on a specified tracker and can be uploaded
  * evict: list items in my library folder that aren't in the database (or delete them)
  * manage your [MusicBrainz "collection"](http://wiki.musicbrainz.org/MusicCollection)