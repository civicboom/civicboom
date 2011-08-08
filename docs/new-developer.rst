Setting up a developer laptop / desktop / a new server
======================================================

First
~~~~~
See the new developer handbook for general information:
https://dev.civicboom.com/redmine/projects/admin/wiki/New_developer_handbook


Running the Site
~~~~~~~~~~~~~~~~
cd src/
make           # bring up menu
make site      # to setup translation files and compile icon map
make test-db   # to init the db and popuplate with test data
make run       # run the site

Using the site
~~~~~~~~~~~~~~
- Setup hosts file
  Add the following line to the bottom of the /etc/hosts file
  127.1.0.1	widget.c.localhost m.c.localhost www.c.localhost
  (netman overwrites 127.0.0.1, and .c.localhost with a 3 part domain
  will map closer to the production env)
  (note: you will need to toggle the cache for each of these domains)
- Connecting
  http://www.c.localhost/
- To sign in
  you can use unittest:password or unitfriend:password
- To sign up
  signup with site
  see console for email debug printouts to get validation url
- CSS development requires caching to be disabled
  this is controlled by a cookie
  visit http://localhost/test/toggle_cache
  this cookie should disable cache for a year or until cookies are cleared
  this needs to be done for all subdomains e.g. widget.localhost if needed

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

