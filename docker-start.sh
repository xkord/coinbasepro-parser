#!/usr/bin/env bash

docker build -t coinbasepro-parser . && docker run --rm -it coinbasepro-parser