
#!/bin/bash
# chkconfig: 2345 20 80
# description: Description comes here....

/usr/bin/x11vnc -loop -nopw -xkb -repeat -noxrecord -noxdamage -forever -rfbport 5900 -display :0&

exit 0
