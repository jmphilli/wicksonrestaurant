#! /bin/bash

pkill gunicorn
gunicorn -w 3 --bind unix:/tmp/gunicorn.sock wsgi &
