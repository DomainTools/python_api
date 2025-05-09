#!/bin/bash

# Script Requirements
# docker

MITM_BASIC_AUTH_CONTAINER_NAME="e2e_test_mitm_basic_auth"
MITM_CUSTOM_CERT_CONTAINER_NAME="e2e_test_mitm_custom_cert"
DOCKER_NETWORK_NAME="e2e_test_docker_network"

echo "Starting e2e tests..."

echo "Create a bridge network for the containers to communicate"
docker network create ${DOCKER_NETWORK_NAME}

echo "Spinning ${MITM_BASIC_AUTH_CONTAINER_NAME}"
docker run --rm -d \
    --name ${MITM_BASIC_AUTH_CONTAINER_NAME} \
    --network ${DOCKER_NETWORK_NAME} \
    -p 8080:8080 mitmproxy/mitmproxy mitmdump \
    --set proxyauth="username:pass"

echo "Spinning ${MITM_CUSTOM_CERT_CONTAINER_NAME}"
docker run --rm -d -v ~/.test_mitmproxy:/home/mitmproxy/.mitmproxy \
    --name ${MITM_CUSTOM_CERT_CONTAINER_NAME} \
    --network ${DOCKER_NETWORK_NAME} \
    -p 8090:8090 mitmproxy/mitmproxy mitmdump \
    --set listen_port=8090

cp ~/.test_mitmproxy/mitmproxy-ca.pem tests/e2e/mitmproxy-ca.pem
python -m pytest -s --capture=sys -v --cov=domaintools tests/e2e

# Clean up from the run
echo "Bringing down containers..."
docker stop ${MITM_BASIC_AUTH_CONTAINER_NAME} || true
docker stop ${MITM_CUSTOM_CERT_CONTAINER_NAME} || true
docker network rm ${DOCKER_NETWORK_NAME} || true

# Clean up custom certs
echo "Removing custom certs..."
rm -rf tests/e2e/mitmproxy-ca.pem
rm -rf ~/.test_mitmproxy
