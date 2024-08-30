#!/bin/sh

if [ -z "$PROXY_PATH" ]; then
    uvicorn fRAGme.app:app --host $HOST --port $PORT
else
    uvicorn fRAGme.app:app --host $HOST --port $PORT --root-path $PROXY_PATH
fi