#!/bin/bash

# Script Requirements
# docker

# Clean up containers
echo "Bringing down containers..."
docker stop ${MITM_BASIC_AUTH_CONTAINER_NAME} || true
docker stop ${MITM_CUSTOM_CERT_CONTAINER_NAME} || true
docker network rm ${DOCKER_NETWORK_NAME} || true

# Clean up custom certs
echo "Removing custom certs..."
sudo rm -rf tests/e2e/mitmproxy-ca.pem
sudo rm -rf ~/.test_mitmproxy
