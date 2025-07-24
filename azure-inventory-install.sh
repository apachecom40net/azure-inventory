#!/bin/bash

# # install azure cli $$ Azure Resource Graph CLI extensions 
# curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
# az extension add --name resource-graph

# # clone this repo in /usr/local/bin

git clone https://github.com/apachecom40net/azure-inventory.git /usr/local/azure-inventory/bin

cd /usr/local/azure-inventory/bin
apt install -y python3.12-venv
python3 -m venv .venv

source /usr/local/azure-inventory/bin/.venv/bin/activate
pip install -r requirements.txt

## move *.sh file Up to be them accecsible through path
mv ./azure-inventory.sh /usr/local/bin/azure-inventory
mv ./azure-inventory-by-subs.sh /usr/local/bin/azure-inventory-by-subs

## make them execiutables
chmod +x /usr/local/bin/azure-inventory
chmod +x /usr/local/bin/azure-inventory-by-subs