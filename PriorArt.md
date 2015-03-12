# Library Management #

Well-respected OSS media players and how they've accomplished library management.

## Banshee ##

Written in C#. [Browse source.](http://svn.gnome.org/svn/banshee/trunk/ng-banshee) Checkout: `svn co http://svn.gnome.org/svn/banshee/trunk/ng-banshee`

  * `Banshee.Services/Banshee.Database/BansheeDbConnection.cs`: pragma synchronous=off for speed
  * `Banshee.Services/Banshee.Database/BansheeDbFormatMigrator.cs` takes care of database initialization (not just migration as name would suggest); schema in InitializeFreshDatabase
    * has TrackID, ArtistID, and AlbumID with correspinding CoreTracks, CoreAlbums, and CoreArtists tables for efficient access to artists/albums; CoreTracks has indexes on ArtistID and AlbumID; CoreArtists and CoreAlbums have indexes on their _names_

## Exaile ##

Written in Python. [Browse source.](http://bazaar.launchpad.net/~exaile-devel/exaile/main/files) Checkout: `bzr branch lp:exaile`

  * Schema in `sql/db.sql`.
    * tracks table primary key is path (which is an integer?! -- what's going on?)
    * like Banshee, also has artist, album tables

## Amarok ##

Written in C++. [Browse source.](http://websvn.kde.org/trunk/extragear/multimedia/amarok/src/collection/) Checkout: `svn co svn://anonsvn.kde.org/home/kde/trunk/extragear/multimedia/amarok/`

  * [half-written architecture document](http://amarok.kde.org/wiki/Development/Architecture)
  * Really convoluted. Will take some time to glean things from.

## Quod Libet ##

[Need to look at this.](http://code.google.com/p/quodlibet/)

## et cetera ##

  * [Alexandria](http://code.google.com/p/alexandrialibrary/)
  * [autotagmp3](http://code.google.com/p/autotagmp3/source/browse/trunk/AutoTag.py)
  * [pymp3tagger](http://bitbucket.org/dyoung418/pymp3tagger/overview/) (sketchy)
  * [music-tag-filler](http://github.com/peo3/music-tag-filler/tree/master)
  * [Ikulo](http://bitbucket.org/hangy/ikulo/overview/)
  * ["Music"](http://bitbucket.org/careytilden/music/overview/)
  * [Hystrix Audio](http://hystrixaudio.sourceforge.net/)
  * [zicbee](http://zicbee.gnux.info/)

# Playback #

Quod Libet has a Gstreamer player module that seems highly refined. It's a very tempting playbook page to steal. They even have gapless working. [Check it out.](http://code.google.com/p/quodlibet/issues/detail?id=49)

# Cloning MPD #

[librmpd](http://librmpd.rubyforge.org/) includes a "fake" MPD server for testing. Interesting! [The file.](http://librmpd.rubyforge.org/svn/trunk/lib/mpdserver.rb)

# Automatic Tagging #

Related autotaggers, mostly in Python:
  * [autotagmp3](http://code.google.com/p/autotagmp3/)
  * [shagger-tagger](http://code.google.com/p/shagger-tagger/)
  * [albumidentify](http://github.com/scottr/albumidentify)
  * [echonest-albumidentify](http://github.com/alastair/echonest-albumidentify)
  * [musollo](http://code.google.com/p/musollo-audio-tagger/) (Java)
  * [brainztag](http://github.com/robinst/brainztag/commits/master)