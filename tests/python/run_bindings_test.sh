#!/usr/bin/env sh

echo ":: Running server in the background." 

nohup python3 server.py > server.log 2>&1 &

python3 client.py 
