Some quick & dirty tests
========================

Done to test some unrealistic extremes, coming up with absolute best
and absolute worst numbers.

Tests done on a ~2GHz single-core bytemark VM

static  = /images/civicboom.png   - static file
n-cache = /misc/titlepage         - nginx cache, ie @cacheable(time=600) decorator
t-cache = ?                       - mako template cache
m-cache = ?                       - dynamic page with parts stored in memcache manually
s-cache = ?                       - dynamic page with sqlalchemy cache enabled
dynamic = /contents?list=article  - fully dynamic page

+---------+--------------+
|         |   Hits/sec   |
|         +------+-------+
|         | http | https |
+=========+======+=======+
| static  | 300* |    10 |
| n-cache | 400* |    10 |
| dynamic |   2  |     1 |
+---------+--------------+

* static files and nginx-cached pages are limited by
  bandwidth; everything else is limited by CPU
