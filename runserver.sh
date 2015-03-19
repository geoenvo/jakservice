#!/bin/bash

cd $(dirname $0)
./bin/python ./jaksafe/manage.py runserver 0.0.0.0:80
