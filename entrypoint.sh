#!/bin/sh

# Load environment variables from .env file
if [ -f /tmp/.env ]; then
    export $(cat /tmp/.env | grep -v ^# | xargs)
fi

if [ -z "$PROXY_PATH" ]; then
    uvicorn fRAGme.app:app --host $HOST --port $PORT
else
    uvicorn fRAGme.app:app --host $HOST --port $PORT --root-path $PROXY_PATH
fi
