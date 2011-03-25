Deployment process
==================

- for pushing all of develop
  - git tag                                        # list tags so you can see the most recent one, and pick a number one higher
  - git flow release start <tag name, eg 0.6.5>
  - <any final changes specific to this release>   # normally nothing needs to be done
  - git flow release finish <tag name>
  - git push --tags                                # push the new tag
  - git push                                       # push the actual changes
  - git checkout develop                           # don't forget to go back to develop before doing more work

- for fixing individual urgent bugs
  - git tag                                        # list tags so you can see the most recent one, and pick a number one higher
  - git flow hotfix start <tag name, eg 0.6.5>
  - <fix the bug>
  - git flow hotfix finish <tag name>
  - git push --tags                                # push the new tag
  - git push                                       # push the actual changes
  - git checkout develop                           # don't forget to go back to develop before doing more work

- wait a couple of minutes for the packages to be built and signed by buildbot
- "sudo apt-get dist-upgrade" on the server

