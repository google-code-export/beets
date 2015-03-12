Regardless of the data backend, we should create an extremely simple (i.e., not Picard) and robust-as-possible autotaggers _for the common cases_. This means we don't necessarily have to worry about striving for 100% accuracy on pathological cases like totally disorganized, untagged, lossy files.

# Use Cases and Designs #

## Downloads with Suspect Tags ##

_I want to download an album and run a single command that imports all the audio files in the (single-album) directory, automatically assigning correct metadata for the album. I can expect the files to be tagged reasonably, but I also expect many errors._

Try these things:

  1. Determine artist and album names from existing metadata. Accomplish this by voting for the correct value of each (protect against small disturbances in metadata). Then perform an approximate string search into MusicBrainz to retrieve the most likely album. This search is parameterized with the number of tracks and the approximate lengths of each track.
  1. If the top result isn't very satisfactory, allow the user to choose from the top few matches.
  1. Prompt user for artist and album names. Use approximate string search as before.
  1. Allow the user to enter manual tags, correcting the current ones. This will account for music that simply isn't/shouldn't be in MusicBrainz.

Flowcharts are dorky, but I made one anyway because this is getting pretty complicated:

![http://wiki.beets.googlecode.com/hg/images/tagflow.png](http://wiki.beets.googlecode.com/hg/images/tagflow.png)

Eventually, we should add fingerprinting: If voting fails (no clear majority) or album cannot be found satisfying requirements with sufficient confidence, resort to MusicBrainz fingerprinting. Get most likely album for each track; again vote to determine the most likely album for the entire set (again parameterized by the number and approximate length of tracks).

### Current Status ###

This tagger is currently implemented as `autotag.tag_album`. The interface thereto is implemented in a few functions in the `ui` module. Currently, the CLI tagger reflects the above flowchart _except for manual tag correction_. That's [Issue 56](http://code.google.com/p/beets/issues/detail?id=56).

The tagger is currently implemented using a pipeline architecture, which helps with modularity and permits parallelism. It uses [my homerolled pipeline module](http://gist.github.com/502867).

Here are some things to do [in the issue tracker](http://code.google.com/p/beets/issues/list?q=component-tagger).

### Evaluation ###

The "quality" of this tagger is very important, but for the moment is very poorly defined. Similarly, we currently have no means of evaluating the speed of the tagger.

It might be a good idea to develop a few datasets consisting of CC-licensed music to evaluate these two criteria. We could measure the accuracy and performance of the tagger for every release to show how we're improving. We could also, for instance, show the performance/accuracy tradeoff afforded by using the fingerprinting plugin. Finally, a benchmark like this might provide a way to compare beets to other taggers (e.g., Picard).

## Improve Tags for Entire Collection ##

More details on this goal are under [Issue 69](http://code.google.com/p/beets/issues/detail?id=69).

## Rip CD ##

Let's forego the canonical sources (freedb) for this kind of data. Probably just query MusicBrainz for DiscIDs. There is a [C extension for getting DiscIDs](http://cddb-py.sourceforge.net/).