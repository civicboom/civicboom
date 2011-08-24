Disaster Recovery Plan
======================

Backups
~~~~~~~
- Off-site backups are taken every 4 hours and archived
  (Using RSync / RSnapshot to automatically log into all the important
  servers and take copies of their files)

- Contains all our important data, so it is stored securely:

  - In the office, behind three locked doors
  - Encrypted hard drive
  - Locked screen


Restoration
~~~~~~~~~~~
- Our central setup server lives in the office
  (Running Puppet)

- Given a set of blank servers, they can be pointed at the setup server and
  they will configure themselves, being ready to go live in around 15 minutes

  - When Amazon's Irish datacenter went down, this process was untested and
    needed polish, so it took about an hour to go from nothing to service as
    normal - since then, we've worked on streamlining the process.

- If the setup server itself is lost, it would need to be reinstalled by
  hand, but this wouldn't affect the live site; the puppet config files
  should all be on the backup server