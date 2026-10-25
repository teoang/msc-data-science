#!/bin/sh
set -eu
cd "$(dirname "$0")"
mkdir -p build
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build Fundamentals_of_Statistical_Learning_Notes.tex
cp build/Fundamentals_of_Statistical_Learning_Notes.pdf ../Fundamentals_of_Statistical_Learning_Notes.pdf
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build Fundamentals_of_Statistical_Learning_Cheatsheet.tex
cp build/Fundamentals_of_Statistical_Learning_Cheatsheet.pdf ../Fundamentals_of_Statistical_Learning_Cheatsheet.pdf
