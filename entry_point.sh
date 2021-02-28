#!/usr/bin/env bash

export FLASK_APP=flask_starter.py
export MAIL_USERNAME=$1
export MAIL_PASSWORD=$2
export FLASKY_ADMIN=$1
export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1

export DEV_DATABASE_URL=postgresql://$3:$4@localhost:5432/flask_store

flask run