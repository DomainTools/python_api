#!/bin/bash

# Script Requirements
# docker

export MITM_BASIC_AUTH_CONTAINER_NAME="e2e_test_mitm_basic_auth"
export MITM_CUSTOM_CERT_CONTAINER_NAME="e2e_test_mitm_custom_cert"
export DOCKER_NETWORK_NAME="e2e_test_docker_network"

echo "Starting e2e tests..."

sh ./tests/e2e/scripts/setup_e2e.sh

echo "E2E processing..."
python -m pytest -s --capture=sys -v --cov=domaintools tests/e2e

sh ./tests/e2e/scripts/cleanup_e2e.sh
