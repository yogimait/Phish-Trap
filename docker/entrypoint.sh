#!/bin/bash
set -e


cleanup() {
    echo "Shutting down services..."
    pkill -f Xvfb
    pkill -f x11vnc
    pkill -f websockify
    pkill -f chromium

    exit 0
}


trap cleanup SIGTERM SIGINT

# Ensure .vnc directory exists with proper permissions
mkdir -p /home/sandbox/.vnc
chmod 700 /home/sandbox/.vnc

# Create required directories with proper permissions
mkdir -p /var/log/supervisor
chown -R sandbox:sandbox /var/log/supervisor


export DISPLAY=:1
export RESOLUTION=${RESOLUTION:-1024x768}


Xvfb $DISPLAY -screen 0 ${RESOLUTION}x16 &
sleep 3  

# Start VNC server without authentication
x11vnc -display $DISPLAY \
    -rfbport $VNC_PORT \
    -forever \
    -shared \
    -noxdamage \
    -noxfixes \
    -noxrecord \
    -nopw \
    -permitfiletransfer no &


websockify --web=/usr/share/novnc/ --heartbeat=30 6080 localhost:$VNC_PORT &

# Start Supervisor as the main process
exec /usr/bin/supervisord -n -c /etc/supervisor/conf.d/supervisor.conf
