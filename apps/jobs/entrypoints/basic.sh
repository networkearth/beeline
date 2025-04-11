#!/bin/bash

mkdir outputs
mkdir inputs

beeline pull-inputs $4 $5

beeline pull-script $1
chmod +x script.R
./script.R

beeline save-outputs $2 $3
