#!/bin/bash

SUBSCRIPTIONS=()

print_usage() {
  echo "Usage:"
  echo "  $0 --subscriptions sub1,sub2,sub3"
  echo "  $0 --from-file subscriptions.txt"
  exit 1
}

if [[ $# -eq 0 ]]; then
  print_usage
fi

while [[ $# -gt 0 ]]; do
  case "$1" in
    --subscriptions)
      IFS=',' read -ra SUBSCRIPTIONS <<< "$2"
      shift 2
      ;;
    --from-file)
      if [[ ! -f "$2" ]]; then
        echo "File not found: $2"
        exit 1
      fi
      mapfile -t SUBSCRIPTIONS < "$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      print_usage
      ;;
  esac
done

# Execute `my_command` for each subscription
for sub in "${SUBSCRIPTIONS[@]}"; do
  echo "Running azure-inventory for subscription: $sub"
  azure-inventory-by-subs --subscription "$sub"
done