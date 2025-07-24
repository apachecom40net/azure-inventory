#!/bin/bash
source /usr/local/azure-inventory/bin/.venv/bin/activate
exec python /usr/local/bin/azure-inventory/bin/azure-inventory.py "$@"
