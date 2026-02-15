#!/bin/bash

# Fehres - Stop Development Infrastructure
# Stops Docker containers started by dev.sh

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${YELLOW}Stopping Fehres Docker infrastructure...${NC}"

# Detect Docker command
if command -v docker &> /dev/null; then
    DOCKER_CMD="docker"
elif command -v docker.exe &> /dev/null; then
    DOCKER_CMD="docker.exe"
else
    echo -e "${RED}Error: Docker not found. Please install Docker or ensure it is in your PATH.${NC}"
    exit 1
fi
echo -e "${BLUE}Using Docker command: $DOCKER_CMD${NC}"

# Stop Docker infrastructure
$DOCKER_CMD compose -f Docker/docker-compose.yml down

echo -e "${GREEN}Infrastructure stopped.${NC}"
echo ""
echo -e "${BLUE}To remove volumes (delete all data):${NC}"
echo -e "  $DOCKER_CMD compose -f Docker/docker-compose.yml down -v"
