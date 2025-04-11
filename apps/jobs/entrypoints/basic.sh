#!/bin/bash

beeline pull-script $1
chmod +x script.R
./script.R
