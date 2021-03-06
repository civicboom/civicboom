Setting up a developer PC
=========================

First
~~~~~
See the new developer handbook for general information, and instructions
for how to get a copy of the code:

https://dev.civicboom.com/redmine/projects/admin/wiki/New_developer_handbook

Once you have the code, read on:


Running the Site
~~~~~~~~~~~~~~~~
::

  cd website/src/
  make clean     # check that everything is fresh defaults
  make site      # to set up translation files and compile icon map
  make test-db   # to init the db and popuplate with test data
  make run       # run the site

(make clean shouldn't be necessary with a fresh checkout, the instruction
is included here for reference when people want to reset their code to a
fresh state)


Demoing the Site
~~~~~~~~~~~~~~~~
::

  cd website/src/
  make clean     # check that everything is fresh defaults
  make site      # to set up translation files and compile icon map
  make demo-db   # to init the db and popuplate with example data
  make run-demo  # run the site in offline mode


Using the site
~~~~~~~~~~~~~~
- Add the following to the bottom of the /etc/hosts file
  ``127.1.0.1 widget.civicboom.lcl m.civicboom.lcl www.civicboom.lcl``
  (netman overwrites 127.0.*.*, and 3 part domain names are needed
  for the URL generator)
- Connect to http://www.civicboom.lcl/
- To sign in you can use unittest:password or unitfriend:password
- To sign up a new account, go through the process as normal except
  looking at the console for email outputs (ie, validation code)
