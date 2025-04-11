#!/bin/bash

beeline pull_script $1
chmod +x script.R
./script.R
