#!/usr/bin/env bash

#\newcommand{\todo}[1]{\textsf{\color{red}{[{TODO: #1}]}}}
#\newcommand{\ray}[1]{\textsf{\color{orange}{[Ray: {#1}]}}}
#\newcommand{\fanz}[1]{\textsf{\color{blue}{[Fan: {#1}]}}}
#\newcommand{\dawn}[1]{\textsf{\color{red}{[Dawn: {#1}]}}}
#\newcommand{\ari}[1]{\textsf{\color{blue}{[Ari: {#1}]}}}
#\newcommand{\anote}[1]{\textsf{\color{red}{[Andrew: {#1}]}}}
#\newcommand{\wh}[1]{\textsf{\color{red}{[Warren: {#1}]}}}
#\newcommand{\weikeng}[1]{\textsf{\color{red}{[Weikeng: {#1}]}}}

for cmd in "todo" "ray" "fanz" "dawn" "ari" "anote" "wh" "weikeng"; do
    grep -n "\\\\$cmd" paper.tex
done

grep "\\\\begin{comment}" paper.tex
