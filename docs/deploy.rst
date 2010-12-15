Deployment process
==================

- push to master
  - git flow release start 1.2.3
  - bump version in the code
  - git commit -a -m "final tweaks"
  - git flow release finish 1.2.3
  - git push --tags master
- wait a couple of minutes for the packages to be built and signed by buildbot
- "sudo apt-get dist-upgrade" on the server

