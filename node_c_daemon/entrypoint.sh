#!/bin/sh
set -e

cat << "EOF"

============================================================
 ██████╗██╗  ██╗██████╗  ██████╗ ███╗   ███╗ █████╗ ██╗      ██████╗ ███╗   ██╗
██╔════╝██║  ██║██╔══██╗██╔═══██╗████╗ ████║██╔══██╗██║     ██╔═══██╗████╗  ██║
██║     ███████║██████╔╝██║   ██║██╔████╔██║███████║██║     ██║   ██║██╔██╗ ██║
██║     ██╔══██║██╔══██╗██║   ██║██║╚██╔╝██║██╔══██║██║     ██║   ██║██║╚██╗██║
╚██████╗██║  ██║██║  ██║╚██████╔╝██║ ╚═╝ ██║██║  ██║███████╗╚██████╔╝██║ ╚████║
 ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝
============================================================
              006 CHROMALON FORGE // LAB TERMINAL ONLINE
              006 CHROMALON FORGE // NNTP ENGINE DEPLOYED
              SYSTEM DEPLOYMENT: MSP/Kerbtap PROTOCOL
============================================================

EOF

# Initialize the custom virtual drive mount point in the background
echo "[VFS Bootstrap] Mounting file conduit at /tmp/nntpfusemount..."
python /root/workspace/nntpfuse.py /tmp/nntpfusemount &

# Execute the master application script
exec python /root/workspace/app.py
