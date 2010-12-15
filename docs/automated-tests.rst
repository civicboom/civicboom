Automated Test Framework
========================

tl;dr: How to write a test
~~~~~~~~~~~~~~~~~~~~~~~~~~
- Standard pylons test framework is used
- run "nosetests" from the $REPO/src/ folder to run manually


Behind the scenes, how it is automated
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Buildbot will automatically build / install / test for every git push, making use of several VMs:

- test-pkgbuild
  - downloads source code and builds packages, uploads to buildmaster
- test-server
  - installs the packages from buildmaster and runs a server
- test-client
  - runs browser-based tests against the server

details
~~~~~~~
- master installed on dev-utils:/home/buildmaster
- config file is ~/cb-master/master.cfg
- after updating the config, "buildbot reconfig ~/cb-master"

