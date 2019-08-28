#!/usr/bin/env bash

for cmd in "todo" "fanz"; do
    grep -n "\\\\$cmd" *.tex
done

grep -n "\\\\begin{comment}" *.tex
