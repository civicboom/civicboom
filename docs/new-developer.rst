Setting up a developer laptop / desktop / a new server
======================================================


Packages
~~~~~~~~
- packages are in a debian repository https://dev.civicboom.com/packages/
- cb-repo package will set this up (it will add the repository to apt
  sources, and add the encryption keys to stop warnings about unsigned
  packages)
  - needs installing by hand
  - download the latest cb-repo*.deb from https://dev.civicboom.com/packages/
  - for gui, double click; for command line, "dpkg -i cb-repo*.deb"
  - apt-get update to fetch the new data
- once the repository has been installed, civicboom packages will be usable
  like any others
  - eg "apt-get install cb-website" will get the code and dependencies
- once the website and dependencies are installed, a developer can clone
  the repository into their home folder and work on it there, running the
  development setup on port 5000


Code Repositories
~~~~~~~~~~~~~~~~~
repositories in dev-utils:/home/code/git, symlinked as /git, so they can
be accessed as ssh://dev.civicboom.com/git/*reponame*

- **website**
  - source for the cb-website package
  - python-cbmisc also lives here (the entire package was 10 lines of
    makefile, so it was merged into the website makefile)
- **android**
  - the android app, minimal files to build from the command line
    - so it can be automated
	- no Eclipse bloat
- **repo**
  - source for the cb-repo package
- **buildmaster**
  - buildmaster config files
- **old-website**
  - the SVN repository, converted to Git, contains all the old stuff for
    reference
- **old-android**
  - the android app, including Eclipse bloat


Database schema
~~~~~~~~~~~~~~~
- A blank database needs to be created that the civicboom user has permission
  to write to
- ./admin_scripts/init_cbdb takes care of this
  - it will destroy any existing data


Geolocation data (Optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~
- fetch the openstreetmap planet data file, eg http://ftp.heanet.ie/mirrors/openstreetmap.org/planet-latest.osm.bz2
  - note, 10GB download, takes a while
  - smaller .osm files are available (eg "kent" or "uk")
- cat planet-latest.osm.bz2 | bunzip2 | ./admin_scripts/osm_to_sql > ./admin_scripts/places.sql
  - wait 10 hours (use "pv" instead of "cat" for a progress bar)
- init_cbdb will then notice the places.sql file and load it when it creates
  the database schema

