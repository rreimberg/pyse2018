#!/bin/bash

cd /source && celery worker -A run_celery -l DEBUG
