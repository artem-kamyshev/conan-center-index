#!/bin/bash

set -e
set -x

cd ./recipes/openssl/ALL && ./build.py
