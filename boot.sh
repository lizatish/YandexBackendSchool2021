#!/bin/sh
source venv/bin/activate
flask run
flask db upgrade
