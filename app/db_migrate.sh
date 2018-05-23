#!/bin/bash

if [ ! "$(ls -A /code/migrations)" ]; then
  flask db init
fi
flask db migrate
flask db upgrade
