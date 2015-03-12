# Packaging #

To make beets more easily available to users it would be nice to create packages / installers for different platforms so that people can get a stable release for beets without having to mess with getting packages from pypi and so on.

Currently beets is very much in development but for a 1.0 release it would be nice if we could have something like this.

An additonal problem could be that some of the python libraries we use are not packaged for the different distributions so we'd need to do that too. That alone makes it a lot more difficult.

---

## Linux ##
About every Linux distribution (except for derivatives) has their own way of handling the installation of software.

### PKGBUILD (Arch Linux) ###
  * https://wiki.archlinux.org/index.php/Python_Package_Guidelines

The current PKGBUILD for beets [here on AUR](http://aur.archlinux.org/packages.php?ID=39577). It's been suggested that we add a dev build (pulling straight for git/hg) as well.

### RPM (RedHat, Fedora, openSuSE, CentOS, Mandriva) ###

### DEB (Debian/Ubuntu and derivatives) ###

I think the best way to make deb packages from distutils/setuptools is using [stdeb](https://github.com/astraw/stdeb). Should probably set up a PPA for Ubuntu users.

  * http://www.debian.org/doc/packaging-manuals/python-policy/
  * http://wiki.debian.org/Teams/PythonAppsPackagingTeam
  * http://wiki.debian.org/Teams/PythonModulesTeam
  * http://python-apps.alioth.debian.org/policy.html

Perhaps we could simplify our lives by using [fpm](https://github.com/jordansissel/fpm). It allows for generation of source-rpm's, debian packages and Solaris packages and can handle python modules.

---

## BSD ##
The BSD-family of operating systems uses a system called ports to provide information to you ports/package-manager on how to download, compile and install software.

  * FreeBSD: http://www.freebsd.org/doc/en/books/porters-handbook/
  * OpenBSD: http://www.openbsd.org/porting.html
  * NetBSD: http://www.netbsd.org/docs/pkgsrc/developers-guide.html

---

## Mac OS X ##
Mac OS X has no unified way of installing extra's into it's Unix base system. A few solutions have been created to remediate the situation.

### MacPorts ###

Here's a [guide to writing portfiles](http://guide.macports.org/#development) for MacPorts.

### brew ###

Here's brew's guide to writing [Formulae](https://github.com/mxcl/homebrew/wiki/Formula-Cookbook).