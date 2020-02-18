#!/bin/bash

set -e
set -x

cd ./recipes/zlib/1.2.11 && python ./build.py
