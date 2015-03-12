# Getting the Source #

The easiest way to get started with the latest beets source is to use [pip](http://pip.openplans.org/) to install an "editable" package. (You will also need [Mercurial](http://mercurial.selenic.com/) installed.) Use this command:
```
$ pip install -e hg+https://beets.googlecode.com/hg/#egg=beets
```
(To install into a virtualenv (probably a good idea), provide the `-E` option to pip.) If you already have a released version of beets installed, you may need to remove it first by typing `pip uninstall beets`. The pip command above will put the beets source in a `src/beets` directory and install the `beet` CLI script to a standard location on your system.

Alternatively, you can get the source via either [Mercurial at Google Code](http://code.google.com/p/beets/source/checkout) or [git at the GitHub mirror](http://github.com/sampsyo/beets). The pip method above installs dependencies automatically, but if you do it manually, you can use pip to install the Python modules `mutagen`, `munkres`, `unidecode`, and `python-musicbrainz2`. With that in place, you can just type `./beet` in the source directory to run beets from there.


# Getting Involved #

Consider joining the [mailing list for beets](http://groups.google.com/group/beets-users). It's fairly low-traffic and is used by both users and developers on the project. Or hang out in the #beets IRC channel on Freenode.


# Contributing as a Non-Programmer #

You can help out with the beets project even if you're not a Python hacker! Here are a few ideas:
  * Promote beets! Help get the word out by telling your friends, writing a blog post, or discussing it on a forum you frequent.
  * A new Web site. [Beets' current site](http://beets.radbox.org/) leaves a little to be desired. If you have design expertise, consider contributing a new homepage for the project.
  * GUI design. For the time being, beets is a command-line-only affair. But that's mostly because I don't have any great ideas for what a good GUI should look like. If you have those great ideas, please get in touch.
  * Benchmarks. I'd like to have a consistent way of measuring speed improvements in beets' tagger and other functionality as well as a way of comparing beets' performance to other tools. You can help by compiling a library of freely-licensed music files (preferably with incorrect metadata) for testing and measurement.


# The Code #

I'll write a more thorough guide to beets' architecture eventually, but for the time being, these resources might be helpful:
  * The docstrings in the code should be somewhat elucidating. Type `pydoc beets.ui`, for instance, to get information about the UI module.
  * This wiki contains a lot of thought about beets' architecture. Take a look at [the pages labeled "Design"](http://code.google.com/p/beets/w/list?q=label:Design).
  * I try to keep a pretty complete short-term roadmap over at the [issue tracker](http://code.google.com/p/beets/issues/list). Try there if you want something to work on, and file any bugs or feature requests.


## Coding Conventions ##

There are a few coding conventions I use in beets that you should probably know about if you want to work on beets:
  * All path names are handled internally as _byte strings_ (not unicode). This is because POSIX operating systems' path names are only reliably usable as byte strings -- even if you request unicode paths, you might still get back bytes. The `bytestring_path` function in the `beets.util` module helps make sure that everything is bytes.
  * Pass every path name trough the `syspath` function (also in `beets.util`) before sending it to any **operating system** file operation (`open`, for example). This is necessary to use long filenames (which, maddeningly, must be unicode) on Windows. This allows us to consistently store bytes in the database but use the native encoding rule on both POSIX and Windows.
  * Similarly, the `displayable_path` utility function converts bytestring paths to a Unicode string for displaying to the user. Every time you want to print out a string to the terminal or log it with the `logging` module, feed it through this function.
  * I'm currently trying to target Python 2.5 as a minimum version -- so if you use the `with` statement, for instance, be sure to do a `__future__` import.

For style, I do my best to adhere to [PEP 8](http://www.python.org/dev/peps/pep-0008/) (but let me know if I get lazy).

Personally, I work on beets with [vim](http://www.vim.org/). Here are some `.vimrc` lines that might help with PEP 8-compliant Python coding:
```
filetype indent on
autocmd FileType python setlocal shiftwidth=4 tabstop=4 softtabstop=4 expandtab shiftround autoindent
```
Consider installing [this alternative Python indentation plugin](http://www.vim.org/scripts/script.php?script_id=974). I also like [pyflakes.vim](http://www.vim.org/scripts/script.php?script_id=2441).