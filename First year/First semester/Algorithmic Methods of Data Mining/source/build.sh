#!/bin/sh
set -eu
cd "$(dirname "$0")"
mkdir -p build
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build Algorithmic_Methods_of_Data_Mining_Notes.tex
cp build/Algorithmic_Methods_of_Data_Mining_Notes.pdf ../Algorithmic_Methods_of_Data_Mining_Notes.pdf
