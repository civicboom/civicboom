Server Security Notes
=====================

Client Side
~~~~~~~~~~~
The standard client is just a web browser, so we aren't adding any
custom software to the customer network

We could develop other software, or other people could develop
some using our API, but this document only covers the website

Network
~~~~~~~
- www. and m. are fully encrypted
- widget. is unencrypted, but no private data is ever sent
- api. is optionally encrypted (we assume developers know what they're doing)

Most websites only encrypt the transfer of username & password,
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
At the system level, standard server security practices are used

- Web server, database, and other parts of the system are kept separate
- There are logs of which administrators are logging in to which
  servers and what they're doing

Data locations
~~~~~~~~~~~~~~
- Live web site:
  Rackspace datacenter in London
- Media:
  Amazon's datacenter in Dublin
- Backups:
  Our office in Kent
- Extra bits:
  Bytemark's datacenter in Manchester
