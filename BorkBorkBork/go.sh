#!/bin/bash

# remove old stuff
rm -rf ../build

# generate files
python manage.py distill-local --collectstatic --force

# copy static-like content
mkdir ../build/data
cp -r ../data/recipes/* ../build/data
zip -r -j -q recipes.zip ../data/recipes/*
cp recipes.zip ../build/data/
