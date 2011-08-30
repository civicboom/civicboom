Disaster Recovery Plan
======================

Backups
~~~~~~~
Off-site backups are taken every 4 hours and archived -
Using RSync / RSnapshot to automatically log into all the important
servers and take copies of their files.

Contains all our important data, so it is stored securely:

- In the office, behind three locked doors
- Encrypted hard drive
- Locked screen
- Network access disabled


Restoration
~~~~~~~~~~~
Our central setup server lives in the office, running Puppet. This server
stores a copy of all the other servers' settings, so that in daily use they
can all be managed from one place, and when setting up a new server all the
setup details can be automatically downloaded in one go.

Given a set of blank servers, they can be pointed at the setup server and
they will configure themselves, being ready to go live in around 15 minutes

If the setup server itself is lost, it would need to be reinstalled by
hand, but this wouldn't affect the live site; the puppet config files
should all be on the backup server


Case study
~~~~~~~~~~
When Amazon's Irish datacenter went down, this process was untested and
needed polish, so it took about an hour to go from nothing to service as
normal - since then, we've worked on streamlining the process. Since the
goal of the process is to automate as much as possible, most of the time
was spent waiting. An approximate timeline:

- 10:00 everyone is in the office, we get them up to speed and try to salvage the servers at Amazon
- 11:00 Amazon don't seem to be recovering, quick discussion over where else to go
- 11:10 sign up with Rackspace, wait for them to confirm payment details
- 11:20 account set up, new servers are booted and pointed to puppet, we wait for them to configure themselves
- 11:30 web / API servers are ready to go automatically, database server needs some extra configuration by hand
- 11:45 all server software is installed and configured, backup data starts to upload
- 12:00 live data is restored, new servers are marked as active and start taking visitors

