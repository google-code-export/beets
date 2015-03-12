# Verification #

  * `pylint -E beets` to check for errors.
  * Run all unit tests (`nosetests`, or `python -m test.testall`, or `python setup.py test`).
  * Check that `setup.py` is up to date (dependencies, version number, etc).
  * Check that `__version__` in root module is up to date.
  * Check that `NEWS` is up to date.
  * Spell-check with [codespell](https://github.com/lucasdemarchi/codespell): `./codespell.py -rq2 data/dictionary.txt ~/beets`
  * Make sure everything is checked in by [browsing source](http://code.google.com/p/beets/source/browse/) and `hg st`.
  * Try all the basic built-in commands and switches on existing _large_ library.
  * Autotag some music, ensuring that at least some has Unicode metadata. (Also import some music without autotagging (`-A`) as it's a completely different codepath.)
  * Run BPD, play some music, including some Unicode.
  * Try all known third-party plugins.
  * Uninstall all dependencies. Install into a virtualenv from a source distribution (`python setup.py sdist; ~/venv/bin/pip install dist/beets-XXX.tar.gz`) and repeat the above.

# Release #

  * Tag the revision in Mercurial (`hg tag 1.0bX`).
  * Submit to PyPI: `python setup.py sdist upload`. Ensure we can install from PyPI: `~/venv/bin/pip install beets`.
  * Upload source distribution to Google Code. Change "Featured" label.

# Announcement #

  * Update [Changelog](Changelog.md).
  * Announce on Twitter ([@b33ts](http://twitter.com/b33ts)).
  * Announce on forums.
  * Email mailing list.
  * Update [Freshmeat listing](http://freshmeat.net/projects/beets/).
  * Update [AUR PKGBUILD](http://aur.archlinux.org/packages.php?ID=39577). (`makepkg -g` generates checksums; `makepkg --source` builds the tarball.)
  * (Eventually:) Update Debian package (PPA?) (using [stdeb](http://github.com/astraw/stdeb)?), MacPorts package.