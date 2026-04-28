#!/bin/bash

cd /Users/isakhaapaniemi/talkies/talkies
source .venv/bin/activate
python app.py &
ngrok http 8080 &
sleep 2
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | python3 -c "import sys,json; print(json.load(sys.stdin)['tunnels'][0]['public_url'])")
open $NGROK_URL
wait