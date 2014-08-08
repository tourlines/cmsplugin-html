#!/bin/bash


export PYTHONPATH=$(dirname $0)
django-admin.py test --settings=test_project.settings $1
