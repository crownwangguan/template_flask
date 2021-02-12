#!/usr/bin/env bash

export FLASK_APP=flask_starter.py
flask db init
flask db migrate -m "all tables"
flask db upgrade
flask run