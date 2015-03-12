Add to this page if you write something inefficient (so you don't have to optimize it if it isn't an issue).

  * cache library options (so they don't need to be fetched every time we need the library directory, for instance)
    * cache `string.Template(lib.options['path_format'])` so it doesn't need to be recreated every time
  * determine whether the current hack for all-column (or even single-column) matching is imposingly slow; if so, explore alternatives:
    * SQLite's full-text search module
    * how do other media managers deal with this?
  * Item could keep a MediaFile around rather than creating it for every read() and write()
  * C implementation of edit distance: [py-editdist](http://www.mindrot.org/projects/py-editdist/)
  * C implementation of bipartite matching (?)
  * memoization of plurality calculation
  * import optimizations:
    * check options as they arrive from MusicBrainz; if one is a good match, don't bother loading the rest
    * somehow skip the UI pipeline stage for matches that don't need confirmation so they can get directly to the copying/applying phase
    * new phase for album art
    * avoid getting tracks for albums with track number mismatch