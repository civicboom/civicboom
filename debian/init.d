#!/bin/sh -e

### BEGIN INIT INFO
# Provides:          cb-website
# Required-Start:    $syslog
# Required-Stop:     $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start cb-website at boot time
# Description:       Run the cb-website pylons app using paster.
### END INIT INFO

. /opt/cb-env/bin/activate

APP=/opt/cb/share/website
UID="--user www-data --group www-data"
# FIXME /tmp should be /var/run
DAE="--daemon --pid-file=/tmp/cb-website.pid --log-file=/var/log/civicboom/pylons.log"

cd $APP

case "$1" in
  start)
    paster serve $UID $DAE production.ini start
    ;;
  stop)
    paster serve $UID $DAE production.ini stop
    ;;
  restart)
    paster serve $UID $DAE production.ini restart
    ;;
  force-reload)
    paster serve $UID $DAE production.ini restart
    ;;
  *)
    echo "Usage: $0 {start|stop|restart|force-reload}"
    exit 1
esac

exit 0
