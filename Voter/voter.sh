#!/bin/bash

if [[ -n $1 && -n $2 ]]; then
    PYTHONPATH=lib/: python src/Voter.py $1 $2
else
    echo Ivalid call, provide the Counter and Validator server addresses
fi

