#!/bin/sh -e

. /opt/cb-env/bin/activate

APP=/opt/cb/share/website
UID=--user www-data --group www-data
DAE=--daemon --pid-file=/var/run/cb-website.pid --log-file=/var/log/civicboom/pylons.log

case "$1" in
  start)
    paster serve $UID $DAE $APP/production.ini start
    ;;
  stop)
    paster serve $UID $DAE $APP/production.ini stop
    ;;
  restart)
    paster serve $UID $DAE $APP/production.ini restart
    ;;
  force-reload)
    paster serve $UID $DAE $APP/production.ini restart
    ;;
  *)
    echo "Usage: $0 {start|stop|restart|force-reload}"
    exit 1
esac

exit 0
