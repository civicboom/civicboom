Automated Test Framework
========================

tl;dr: How to write a test
~~~~~~~~~~~~~~~~~~~~~~~~~~
- Standard pylons test framework is used
- run "make test-db" from the $REPO/src/ folder to run manually


Behind the scenes, how it is automated
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Buildbot will automatically build / install / test for every git push, making use of several VMs:

- test-build32 / test-build64
  - downloads source code and builds packages, uploads to buildmaster
- test-server
  - installs the packages from buildmaster and runs a server
- test-client (dead, work is in progress for a selenium grid)
  - runs browser-based tests against the server

details
~~~~~~~
- master installed on dev:/home/buildmaster
- config file is ~/cb-master/master.cfg
- after updating the config, "buildbot reconfig ~/cb-master"
