Civicboom CDN Setup
===================

When buildbot builds a master package, it also runs cdnpush; this syncs
src/civicboom/public/ with bm1:/opt/cb/var/www/static/${git-tag-version}/.

The package build process creates src/.version with the git version

In app_globals, we check for .version

If app_globals.version is set, we load static files from bm1:/$version/,
if not, we load from $host/
