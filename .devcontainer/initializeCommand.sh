#!/bin/bash

ROOT_DIR_PATH=$(git rev-parse --show-toplevel)
DOCKER_IMAGE="darknessoup/petalinux-2019.2:20240703_1" # Add petalinux image from dockerhub here

# ensure user and Ids are correct
USER=$(whoami)

DEV_CONTAINER_FOLDER="${ROOT_DIR_PATH}/.devcontainer"
export DOCKER_IMAGE_NAME="petalinux-${USER}"
docker build -f ${DEV_CONTAINER_FOLDER}/Dockerfile \
    --build-arg DOCKER_IMAGE="${DOCKER_IMAGE}" \
    --build-arg USERNAME="${USER}" \
    --build-arg USER_UID="$(id -u)" \
    --build-arg USER_GID="$(id -g)" \
    -t ${DOCKER_IMAGE_NAME} .

