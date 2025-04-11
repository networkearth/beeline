#!/bin/bash

beeline pull-script $1
chmod +x script.R
./script.R
beeline save_outputs $2 $3
