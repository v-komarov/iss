#!/bin/sh

# Your Zenoss server settings.
# The URL to access your Zenoss5 Endpoint
ZENOSS_URL="http://10.6.0.129:8080"

ZENOSS_USERNAME=$6
ZENOSS_PASSWORD=$7


# Generic call to make Zenoss JSON API calls easier on the shell.
    ROUTER_ENDPOINT=$1
    ROUTER_ACTION=$2
    ROUTER_METHOD=$3
    DATA=$4
    FILE=$5

    if [ -z "${DATA}" ]; then
        echo "Usage: zenoss_api <endpoint> <action> <method> <data>"
        return 1
    fi
# add a -k for the curl call to ignore the default cert
    curl \
        -k \
        -u "$ZENOSS_USERNAME:$ZENOSS_PASSWORD" \
        -X POST \
        -H "Content-Type: application/json" \
        -d "{\"action\":\"$ROUTER_ACTION\",\"method\":\"$ROUTER_METHOD\",\"data\":[$DATA], \"tid\":1}" \
        -o $FILE \
        "$ZENOSS_URL/zport/dmd/$ROUTER_ENDPOINT" 

