Server Scaling Notes
====================

Web Services
~~~~~~~~~~~~
Pretty much every aspect of the site scales well (see network.svg) - for web
and API servers, the amount of traffic we can handle is approximately
proportional to the number of servers we have running (which is itself
proportional to hosting costs). For short term traffic spikes, most load
problems can be lifted by running extra servers until the spike is over.

Database
~~~~~~~~
The only bit that isn't trivial is the users & content database, as all the data
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

Based on experience with other projects, I would estimate that a dedicated
database server with SSDs should handle 5000, maybe even 10,000 concurrent
users before we hit a wall with disk speed. It would be a pretty expensive
single server though, where everything else is clusters of cheap parts.
