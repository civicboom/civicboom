Civicboom CDN Setup
===================

When buildbot builds a master package, it also runs cdnpush; this syncs
``src/civicboom/public/`` with rackspace cloud files.

The package build process creates ``src/.version`` with the git version

In app_globals, we check for ``.version``

If app_globals.version is set, load static files from ``cloudfiles:/$version/``,
if not, we load from ``$host/``
