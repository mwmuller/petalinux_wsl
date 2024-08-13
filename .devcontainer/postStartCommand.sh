#!/bin/bash

# Check if petalinux is installed then source the settings file
ROOT_DIR=$(git rev-parse --show-toplevel)
echo "${ROOT_DIR}"
PETALINUX_DIR="$ROOT_DIR/petalinux-tools"

sudo ln -sf /bin/bash /bin/sh

echo "$PETALINUX_DIR"

if [[ -d "${PETALINUX_DIR}" ]]; then
    cd $PETALINUX_DIR
    source ${PETALINUX_DIR}/settings.sh
    echo "source ${PETALINUX_DIR}/settings.sh" >> ~/.bashrc
else
    echo "Petalinux Tools not yet created. Sourcing 'settings.sh' failed."
fi

export PATH="${PETALINUX_DIR}":$PATH
