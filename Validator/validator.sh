#!/bin/bash

if [[ -n $1 ]]; then
    PYTHONPATH=lib/: python src/Validator.py $1
else
    echo 'Invalid server call, provide local IP address arguments for Counter and Validator'
fi

