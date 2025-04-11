#!/usr/bin/env Rscript

print("Welcome to R World!")

file.show("inputs/input1.txt")
file.show("inputs/subdir/input2.txt")

cat("Write to a File", file="outputs/outfile.txt", sep="\n")