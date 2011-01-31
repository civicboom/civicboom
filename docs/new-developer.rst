Setting up a developer laptop / desktop / a new server
======================================================

Things for a sysadmin to do
~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Add unix user to dev server, and add to developers group
    adduser <username>
    adduser <username> developers
- Give them access to the dev website
    htpasswd /home/code/htpasswd <username>
- Set up a google account
    https://www.google.com/a/cpanel/civicboom.com/
- Give them access to redmine
    https://dev.civicboom.com/redmine/users/new


Packages
~~~~~~~~
- packages are in a debian repository https://dev.civicboom.com/packages/
- go there, download the latest cb-repo package, install it by hand, it
  will take care of the rest of the repository setup
- once the repository has been installed, civicboom packages will be usable
  like any others
  - "apt-get update" to fetch the latest package list
  - "apt-get install cb-website" will get the code and dependencies and set
    up a server running locally
  - "apt-get install cb-devkit" will get the things that are not necessary
    to run the site, but are used when building packages
  - "apt-get upgrade" to upgrade all installed parts
- once the website and dependencies are installed, a developer can clone
  the repository into their home folder and work on it there, running the
  development setup on port 5000
  - from src
  - once, "make site" to compile some static bits (eg language translations)
  - "make test-db" to wipe the DB and fill it with test data
  - "make run" to run in development mode

- when working on themes, the developer will probably want to turn off the
  caching of static files
  - sudo gedit /etc/nginx/sites-enabled/civicboom.com
    comment out:
	# proxy_cache "cb";
	# proxy_cache_key "$scheme://$host$request_uri-cookie:$cookie_civicboom_logged_in";

- for working on extra subdomains (widget / mobile):
  - sudo gedit /etc/hosts
    add some entries to the 127.0.0.1 line if using localhost:
    127.0.0.1    localhost.localdomain localhost widget.localhost mobile.localhost m.localhost
	(or your VM's IP address if working on a VM)


Using the site
~~~~~~~~~~~~~~
- To sign in
  you can use unittest:password
- To sign up
  signup with site
  see console for email debug printouts to get validation url


Code Repositories
~~~~~~~~~~~~~~~~~
repositories are in dev:/home/code/git, symlinked as /git, so they can be
accessed as ssh://dev.civicboom.com/git/*reponame*

git clone ssh://dev.civicboom.com/git/*reponame*

- **website**
  - source for the cb-website-* packages
  - python-cbmisc also lives here (the entire package was 10 lines of
    makefile, so it was merged into the website makefile)
- **mobile**
  - the android app, minimal files to build from the command line
    - so it can be automated
	- no Eclipse bloat
- **repo**
  - source for the cb-repo package
- **devkit**
  - source for the cb-devkit package
- **buildmaster**
  - buildmaster config files

get checkout -b develop origin/develop


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
- "make test-db" will then notice the data file and load it when it creates the
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


Running the Site
~~~~~~~~~~~~~~~~

cd src/

make
(bring up menu)

make site 
(to setup translation files)

make test-db to init the db and popuplate with test data
