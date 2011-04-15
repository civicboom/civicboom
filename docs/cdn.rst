Civicboom CDN Setup
===================

When buildbot builds a master package, it also runs cdnpush; this syncs
src/civicboom/public/ with s3:public/${git-tag-version}/.

The package build process creates src/.version with the git version

In app_globals, we check for .version

If app_globals.version is set, we load static files from s3:public/$version,
if not, we load from the app server


