Server Security / Reliability Notes
===================================

Client Side
~~~~~~~~~~~
- The standard client is just a web browser, so we aren't adding any
  custom software to the customer network
  - We could develop other software, or other people could develop
    some using our API, but this document only covers the website

Network
~~~~~~~
- www. and m. are fully encrypted
- widget. is unencrypted, but no private data is ever sent
- api. is optionally encrypted (we assume developers know what they're doing)

  - Most websites only encrypt the transfer of username & password,
    then send the data back and forth in the clear; this is like
    having an armoured garage to get in and turn the car on, then
	parking outside with the engine still running.

Server Side
~~~~~~~~~~~
- Content in our database is marked as public or private, private
  content only shows up to the creator and people the creator has
  allowed
- Media (videos, photos, etc) is stored in Amazon S3; files are
  associated with a 256-bit key which you can only know if you
  access to the file
- There is an event log / audit trail which shows who has edited what
  content, so if a user's account is broken into (eg they were using a
  weak password which got guessed) we can see what the attacker has done
  and have some clues as to who they are

Back-End
~~~~~~~~
- At the system level, standard server security practices are used
  - Web server, database, and other parts of the system are kept separate
  - There are logs of which administrators are logging in to which
    servers and what they're doing


Backups
~~~~~~~
- Off-site backups are taken every 4 hours and archived


Data locations
~~~~~~~~~~~~~~
- Live web site:
  - Rackspace datacenter in London
- Media:
  - Amazon's datacenter in Dublin
- Backups:
  - Our office in Kent
- Extra bits:
  - Bytemark's datacenter in Manchester


Reliability
~~~~~~~~~~~
- With multiple servers, they can be taken out of action one at a time, upgrades
  done, and put back into service; that way, the service as a whole is always up
  - Alterations to the database schema require all database servers to be updated
    at once
- With multiple servers, errors can be automatically detected and a crashed server
  can be routed around

- If a server is rebooted in a controlled way, uploads in progress can be allowed
  to finish; if it crashes, they will need restarting
  - Article text is saved as drafts, so a lost connection won't lose everything


Scaling
~~~~~~~
- Pretty much every aspect of the site scales well (see network.svg)

- The only bit that isn't trivial is the users & content database, as all the data
  is inter-related, frequently updated, and needs to be kept in sync
  - the simplest way to deal with this is to avoid touching the database; simple
    reads should be cached inside pylons, or with memcache, or somesuch
  - read-only slaves can handle the more complex queries, at the cost of a few ms
    lag in updates
  - non-urgent data writes (eg, page view counts) can be queued and written in
    batches
  - data writing speed can be scaled by using faster disks, RAID, SSDs, splitting
    tables over multiple disks, etc; but each increase in speed is more expensive
    than the last, and is ultimately limited to a single server
    - Based on experience with other projects, I would estimate that a dedicated
      database server with SSDs should handle 5000, maybe even 10,000 concurrent
      users before we hit a wall with disk speed. It would be a pretty expensive
      single server though, where everything else is clusters of cheap parts.

