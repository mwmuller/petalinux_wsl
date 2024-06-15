#!/bin/bash

ROOT_DIR_PATH=$(git rev-parse --show-toplevel)
DOCKER_IMAGE="ubuntu:18.04"

# ensure user and Ids are correct
USER=${USER:-${whoami}}

DEV_CONTAINER_FOLDER="${ROOT_DIR_PATH}/.devcontainer"
export DOCKER_IMAGE_NAME="petalinux-${USER}"
docker build ${DEV_CONTAINER_FOLDER} \
    --build-arg DOCKER_IMAGE="${DOCKER_IMAGE}" \
    --build-arg USERNAME="${USER}" \
    --build-arg USER_UID="$(id -u)" \
    --build-arg USER_GID="$(id -g)" \
    -t ${DOCKER_IMAGE_NAME}
