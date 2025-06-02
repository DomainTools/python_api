#!/bin/bash

# Script Requirements
# docker

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

# Check until custom cert from mitmproxy container is copied locally
echo "Checking for valid custom cert..."
while [ ! -f ~/.test_mitmproxy/mitmproxy-ca.pem ] ;
do
    sleep 2
done
echo "Valid custom cert found!"

# Copy valid custom cert to target dir
docker cp ${MITM_CUSTOM_CERT_CONTAINER_NAME}:/home/mitmproxy/.mitmproxy/mitmproxy-ca.pem ./tests/e2e/mitmproxy-ca.pem
