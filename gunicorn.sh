#! /bin/bash

gunicorn -w 3 --bind unix:/tmp/gunicorn.sock wsgi &
