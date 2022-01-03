#!/bin/bash

echo "Static server 'server.sh' must be running for this to work"

rm -rf search-output
python -m Static-Site-Search --urls http://127.0.0.1:8000/ --output search-output
cp search-output/* build/searcher/
