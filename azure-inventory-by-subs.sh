#!/bin/bash
source /usr/local/bin/azure-inventory/.venv/bin/activate
exec python /usr/local/bin/azure-inventory.py "$@"