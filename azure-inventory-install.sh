#!/bin/bash

# install azure cli $$ Azure Resource Graph CLI extensions 
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
az extension add --name resource-graph

# clone this repo in /usr/local/bin
