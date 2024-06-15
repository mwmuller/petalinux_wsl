#!/bin/bash

# Runningthe petalinux sh from support.xilinx.com/s/article/73296
cd scripts/

sudo ./plnx-env-setup.sh

PTLNX_FOLDER="petalinux-tools"
mkdir ${PTLNX_FOLDER}
if [[ -d "$PTLNX_FOLDER" ]]; then
    echo "$PTLNX_FOLDER created..."
    cd petalinux-tools
else
    echo "Filed to create ${PTLNX_FOLDER}"
    exit 1
fi

sudo ../petalinux-v2019.2-final-installer.run 

source ./settings.sh

