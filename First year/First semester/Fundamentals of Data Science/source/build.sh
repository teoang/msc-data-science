#!/bin/sh
set -eu
cd "$(dirname "$0")"
mkdir -p build
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build Fundamentals_of_Data_Science_Notes.tex
cp build/Fundamentals_of_Data_Science_Notes.pdf ../Fundamentals_of_Data_Science_Notes.pdf
