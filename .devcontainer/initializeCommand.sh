#!/bin/bash

set -eo pipefail

ROOT_DIR_PATH="$(git rev-parse --show-toplevel)"

touch ${HOME}/.netrc

USER=${USER:-${whoami}}
DEV_CONTAINER_FOLDER="${ROOT_DIR_PATH}/.devcontainer"

echo "${USER}"
docker build ${DEV_CONTAINER_FOLDER} \
    --build-arg USERNAME="${USER}" \
    --build-arg USER_UID="$(id -u)" \
    --build-arg USER_GID="$(id -g)"