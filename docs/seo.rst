Civicboom Search Engine Things
==============================

Implemented code
~~~~~~~~~~~~~~~~
Members have hCard attributes to identify them as a person
 - Nickname (username)
 - Title, Forename, Surname (guessed from name)
 - Organisation, Role (if they are a member of a hub, this hub and role
   will be listed; if not, they get "Civicboom: Member")

Groups have hCard attributes to identify them as organisations
 - Nickname (username)
 - Name (name)

Members have links to their google profiles (and other)
 - ``<a rel="me" href="...">My Profile on website Foo</a>``

Content have their author listed
 - ``Written by <a rel="author" href="/members/bob">Bob</a>``


Practical Results
~~~~~~~~~~~~~~~~~
Member:hCard = user's avatar and membership details show in search results
for the member

Content -> Author -> Google Profile chain = user's avatar shows up on google
search results for the content


Links
~~~~~
- http://www.google.com/webmasters/tools/richsnippets
- http://microformats.org/wiki/hcard
- http://www.google.com/support/webmasters/bin/answer.py?answer=1229920&hl=en
