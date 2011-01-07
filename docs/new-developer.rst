Setting up a developer laptop / desktop / a new server
======================================================

Things for a sysadmin to do
~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Add unix user to dev server, and add to developers group
    adduser <username>
    adduser <username> developers
- Give them access to the dev website
    htpasswd /home/code/htpasswd <username>
- Give them access to redmine
    https://dev.civicboom.com/redmine/users/new


Packages
~~~~~~~~
- packages are in a debian repository https://dev.civicboom.com/packages/
- go there, download the latest version of cb-repo, install it by hand
- once the repository has been installed, civicboom packages will be usable
  like any others
  - "apt-get update" to fetch the latest package list
  - "apt-get install cb-website" will get the code and dependencies
  - "apt-get install cb-devkit" will get things necessary to build packages
  - "apt-get upgrade" to upgrade all installed parts
- once the website and dependencies are installed, a developer can clone
  the repository into their home folder and work on it there, running the
  development setup on port 5000


Code Repositories
~~~~~~~~~~~~~~~~~
repositories are in dev:/home/code/git, symlinked as /git, so they can be
accessed as ssh://dev.civicboom.com/git/*reponame*

- **website**
  - source for the cb-website-* packages
  - python-cbmisc also lives here (the entire package was 10 lines of
    makefile, so it was merged into the website makefile)
- **android**
  - the android app, minimal files to build from the command line
    - so it can be automated
	- no Eclipse bloat
- **repo**
  - source for the cb-repo package
- **devkit**
  - source for the cb-devkit package
- **buildmaster**
  - buildmaster config files


Database schema
~~~~~~~~~~~~~~~
- A skeleton database needs to be created
  - in admin_scripts, "./init_cbdb"
- To populate the database with the base data
  - in src, "paster setup-app development.ini"
- To add example data, by testing the system
  - in src, "nosetests"



Geolocation data (Optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~
- fetch an openstreetmap data file, eg
  - http://download.geofabrik.de/osm/europe/great_britain/england/kent.osm.bz2
    - Kent only, 10MB, good for testing
  - http://downloads.cloudmade.com/europe/united_kingdom/united_kingdom.osm.bz2
    - UK only, 350MB
  - http://ftp.heanet.ie/mirrors/openstreetmap.org/planet-latest.osm.bz2
    - full planet, 10GB, decompresses to ~200GB and takes several days to load
- place the .osm.bz2 file in admin_scripts/
- init_cbdb will then notice the data file and load it when it creates the
  base databases


Git Setup
~~~~~~~~~
- making use of the git branching model
  - http://nvie.com/posts/a-successful-git-branching-model/
- using the gitflow scripts to manage
  - https://github.com/nvie/gitflow
- see git-flow.svg for a diagram with gitflow commands added

In a nutshell; the "master" branch should always be production-ready; the
developers create branches off of "develop" and then merge back into it.
When "develop" is close to stable, a "release" branch is formed for final
tweaks (eg, setting the version number), and then pushed to master.

For emergency fixes of production code, a "hotfix" branch can come off
of master, have the fix written and tested, and then the fix is merged into
both master and develop.


Recommended tweaks to $REPO/.git/config:

 # Set your civicboom account here; this can also go in the global
 # ~/.gitconfig rather than per-project
 [user]
     name = Name Goes Here
     email = n.here@civicboom.com
 [color]
     ui = auto

 # Turn off fast-forward merging, so that full history is preserved:
 [branch "develop"]
     mergeoptions = --no-ff

