#!/bin/sh
#
# init script for clock1
#

### BEGIN INIT INFO
# Provides:          clock1
# Required-Start:    $remote_fs $syslog $network
# Required-Stop:     $remote_fs $syslog $network
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: init script for the clock1 app
# Description:       We'll have to fill this out later...
### END INIT INFO

STATE="error";
COUNT=0

PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
NAME=clock1
DAEMON=/home/pi/coding/AlexClock/clock1.py
DAEMONARGS=""
PIDFILE=/var/run/$NAME.pid
LOGFILE=/var/log/$NAME.log

. /lib/lsb/init-functions

test -f $DAEMON || exit 0

case "$1" in
    start)
        start-stop-daemon --start --background \
            --pidfile $PIDFILE --make-pidfile --startas /bin/bash \
            -- -c "exec stdbuf -oL -eL $DAEMON $DAEMONARGS > $LOGFILE 2>&1"
        log_end_msg $?
        ;;
    stop)
        start-stop-daemon --stop --pidfile $PIDFILE
        log_end_msg $?
        rm -f $PIDFILE
        ;;
    restart)
        $0 stop
        $0 start
        ;;
    status)
        start-stop-daemon --status --pidfile $PIDFILE
        log_end_msg $?
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 2
        ;;
esac

exit 0