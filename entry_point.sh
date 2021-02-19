#!/usr/bin/env bash

export FLASK_APP=flask_starter.py
export MAIL_USERNAME=$1
export MAIL_PASSWORD=$2
export FLASKY_ADMIN=$1

flask run