#!/usr/bin/env bash

for cmd in "todo" "fanz"; do
    grep -n "\\\\$cmd" paper.tex
done

grep "\\\\begin{comment}" paper.tex
