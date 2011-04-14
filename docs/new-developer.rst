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
- Connecting
  http://localhost:5000/
- To sign in
  you can use unittest:password or unitfriend:password
- To sign up
  signup with site
  see console for email debug printouts to get validation url
- CSS development requires caching to be disabled
  this is controlled by a cookie
  visit http://localhost/test/toggle_cache
  this cookie should disable cache for a year or until cookies are cleared

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

