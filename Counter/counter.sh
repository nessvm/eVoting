#!/bin/bash

if [[ -n $1 ]]; then
    PYTHONPATH=lib/: python src/Counter.py $1
else
    echo 'Invalid server call, provide local IP address for the server'
fi

