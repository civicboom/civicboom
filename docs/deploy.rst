Deployment process
==================

- push to master
  - git tag                                        # - list tags so you can see the most recent one, and pick a number one higher
  - git flow release start <tag name, eg 0.6.5>    # - between start and finish you could do final tweaks, eg incrementing the
  - git flow release finish <tag name>             #   version number in a README file, but we don't need to do anything
  - git push --tags                                # - push the new tag
  - git push                                       # - push the actual changes
  - git checkout develop                           # - don't forget to go back to develop before doing more work
- wait a couple of minutes for the packages to be built and signed by buildbot
- "sudo apt-get dist-upgrade" on the server
  - "sudo /etc/init.d/cb-website restart" needs doing to restart the paster process, this should be automated

