Server Reliability Notes
========================

Back-end
~~~~~~~~
Using a network of multiple web servers and multiple database servers

- They can be taken out of action one at a time, upgrades done, and put back
  into service; that way, the service as a whole is always up
  (However, large alterations to the database schema require all database servers
  to be updated at once)
- Errors can be automatically detected and a crashed server
  can be routed around
- If a web server goes down, a replacement can be set up within minutes of
  an administrator being online to deal with it (this process could be
  automated, but then a bug in the automator may endlessly start new servers
  and generate a huge bill -- since failures are relatively rare, and when
  they do happen they're big enough to require human intervention anyway,
  leaving the process as a manual one seems like a sensible decision for now)
- Currently if our primary database server goes down, switching over to the
  secondary is a manual process that will take a few minutes -- the next
  versions of our database software are set to include a lot of useful tools
  for automatic failover, so we will upgrade to them as soon as they're ready

Front-end
~~~~~~~~~
If a server is rebooted in a controlled way, uploads in progress can be allowed
to finish; if it crashes, they will need restarting

Article text is saved as drafts, so a lost connection won't lose everything
