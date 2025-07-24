#!/bin/bash
source /usr/local/bin/azure-inventory/bin/activate
exec python /usr/local/bin/azure-inventory/bin/azure-inventory.py "$@"