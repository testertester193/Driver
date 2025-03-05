#!/bin/bash
gunicorn driver:server --bind 0.0.0.0:10000