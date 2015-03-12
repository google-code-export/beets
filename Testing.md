# Running the Tests #

If you have [nose](http://somethingaboutorange.com/mrl/projects/nose/), just run `nosetests` in the beets repository. Otherwise, `cd test` and then `./testall.py`.

# Needs testing #

  * library options
  * browsing functions (artists, albums, items) AND their naive implementations
  * MusicBrainz -- need to mock the web service. [This version](http://code.google.com/p/beets/source/detail?r=28db18222b5589f2b49007db6a3dcefac0b705a2) has some tests that should be reinstated once the WS is mocked out.
  * UI code -- this breaks all the time. Need a good way to mock the filesystem.

# Refinements #

It would be nice to get rid of the `rsrc` directory with all the sample files in it and instead just include the relevant metadata somewhere. A nice mock filesystem would also be convenient.

# Red Flags #

`coverage run --source=beets testall.py` (We're at about 60% coverage right now -- not too good! There are some pretty obvious things to cover, too.)

`python -3 testall.py` (Raises a few warnings, and a _lot_ of warnings for Mutagen. Right now, the warnings are: buffer has been replaced with memoryview in py3k, and we use some integer division. Python 2.6 supports `b''` literals, but Python 2.5 doesn't.

Use [unicode-nazi](http://pypi.python.org/pypi/unicode-nazi).