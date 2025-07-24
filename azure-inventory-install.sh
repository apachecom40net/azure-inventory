#!/bin/bash

# # install azure cli $$ Azure Resource Graph CLI extensions 
# curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
# az extension add --name resource-graph

# # clone this repo in /usr/local/bin

git clone https://github.com/apachecom40net/azure-inventory.git /usr/local/bin/azure-inventory/bin

cd /usr/local/bin/azure-inventory/bin
apt install -y python3.12-venv
python3 -m venv .venv

source ./.venv/bin/activate
pip install -r requirements.txt

## move *.sh file Up to be them accecsible through path
mv ./azure-inventory.sh ../../azure-inventory
mv ./azure-inventory-by-subs.sh ../../azure-inventory-by-subs

## make them execiutables
chmod +x ../../azure-inventory
chmod +x ../../azure-inventory-by-subs
