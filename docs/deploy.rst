Deployment process
==================

- make a commit, push to the dev server
- wait a couple of minutes for the packages to be built and tested by buildbot
- manually run deploy-alpha, deploy-beta, or deploy-live

For typo fixes deploy-live might be ok, for major changes deploy-alpha to
let the rest of the team test, then deploy-beta to let the public test,
then deploy-live when confident of stability
