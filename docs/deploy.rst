Deployment process
==================

Push to master to build packages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

for pushing all of develop
--------------------------
::

  git tag                                        # list tags so you can see the most recent one, and pick a number one higher
  git flow release start <tag name, eg 0.6.5>
  <any final changes specific to this release>   # normally nothing needs to be done
  git flow release finish <tag name>
  git push origin master <tag name>              # push the new tag and associated changes
  git checkout develop                           # don't forget to go back to develop before doing more work

for fixing individual urgent bugs
---------------------------------
::

  git tag                                        # list tags so you can see the most recent one, and pick a number one higher
  git flow hotfix start <tag name, eg 0.6.5>
  <fix the bug>
  git flow hotfix finish <tag name>
  git push origin master <tag name>              # push the new tag and associated changes
  git checkout develop                           # don't forget to go back to develop before doing more work



Install the packages
~~~~~~~~~~~~~~~~~~~~

- wait a couple of minutes for the packages to be built and signed by buildbot


Get a list of servers
---------------------

- as of this writing we have webapi1, webapi2, db1, db2.civicboom.com
- for a realtime list, log into the rackspace control panel

  - https://lon.manage.rackspacecloud.com/pages/Login.jsp
  - civicboom
  - hosting -> cloud servers -> server instances


upgrade the servers (web / api nodes)
-------------------------------------

- ssh into the server
- ``cb-install``, then follow prompts to upgrade (or downgrade) the installed packages
- check that the site is working by viewing that specific server (eg http://webapi2.civicboom.com/contents.json).
  Doing one at a time means that the load balancer always has at least one active server to point to


upgrade the servers (database nodes)
------------------------------------
- note that the database rarely needs updating, and doing it is a pain, so
  most of the time I leave it as is
- on your dev box

  - ``make schemadiff``
  - view update.sql

- schema updating is a PITA; if there are updates to be made, it may be
  a good idea to do it in an off-peak period
- large alterations (dropping / creating tables, etc) may require locking
  the database, which pretty much means you need to disconnect other users
  (ie, log into the API nodes and turn them off during the upgrade. Don't
  forget to turn them back on once it's done!)

- log in as above
- ``cb-install`` to upgrade packages
- ``psql -U civicboom -h localhost civicboom``, then run the commands in update.sql

