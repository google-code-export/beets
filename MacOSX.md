# Introduction #

We've run into a problem or two with beets on Mac OS X, this page documents that and possible work-arounds.

# Importing over the network #

This is a particularly nasty bug.

Samba, the suite of tools Mac OS X prior to Lion has on board to communicate over SMB/CIFS (Windows file sharing) has problems communicating pathnames that include non-ASCII characters.

According to the Samba Administration Guide:
> Although Mac OS X uses UTF-8 as its encoding method for filenames, it uses an extended UTF-8 specification that Samba cannot handle, so UTF-8 locale is not available for Mac OS X.

This has a very simple yet frustrating consequence: If you are doing a `beet import` on files that are accessed over Samba and those files have characters in their names that contain accented or otherwise exotic characters the import will fail and you'll get errors.

Somehow though the Samba documentation seems to be out of date. Specifying a `unix charset = UTF-8` on a Debian samba server and then running: `beet import Með\ suð\ í\ eyrum\ við\ spilum\ endalaust/` from a Mac worked however it has failed in other scenario's with file paths including, for example, the "é" character.

**Recently a similar issue has been observed when files are getting accessed over AFP which has sparked the idea that it might have to do with how beets handles the options passed on the command-line.**

# ReplayGain #

In order to use the ReplayGain plugin a few things need to be installed. Mainly the dependency on gstreamer is a bit tricky on OS X.

Unfortunately you'll have to build it yourself. Now you can torture yourself for ages trying or use something like MacPorts, fink or brew (very much recommend brew) to install it.

Please note that installing gstreamer and the python bindings are not enough. We also need all the gst-plugins-**in order for ReplayGain to work.**

## Brew ##

Brew has the current (2011-06-08) disadvantage that the python bindings haven't been included yet. In any case, you'll need to do something like this:

```
brew install gstreamer
```

After that, you can build gst-python yourself if it hasn't been added to brew by then. The sources can be found here: http://gstreamer.freedesktop.org/src/gst-python/

## MacPorts ##

MacPorts should be something along the lines of this:
```
sudo port selfupdate
sudo port install py26-gst-python
```

## Gstreamer plugins ##
You'll need the following gstreamer plugins too:
```
gst-plugins-base
gst-plugins-bad
gst-plugins-good
gst-plugins-ugly
```

Those plugins are available in MacPorts, brew and fink.