#!/bin/bash
source ~/azure-inventory/.venv/bin/activate
exec python ~/azure-inventory/azure-inventory.py "$@"