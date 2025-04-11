#!/bin/bash

mkdir output
mkdir input

beeline pull-script $1
chmod +x script.R
./script.R
beeline save-outputs $2 $3
