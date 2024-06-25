#!/bin/bash

# Running the petalinux sh from support.xilinx.com/s/article/73296
CREATE_INSTALL="true"
PETALINUX_INSTALLER=${1:-"petalinux-v2019.2-final-installer.run"}
PTLNX_FOLDER="petalinux-tools"
if [[ -d "$PTLNX_FOLDER" ]]; then
    echo "$PTLNX_FOLDER Folder alredy created do you want to delete it and re-install? [y/n]"
    read SELECTION
    if [[ "$SELECTION" == "y" ]]; then
        CREATE_INSTALL="true"
        echo "Removing tools folder"
        rm -rf "$PTLNX_FOLDER"
    else
        echo "Exitting..."
        exit 1
    fi
fi

mkdir ${PTLNX_FOLDER} 
if [[ -d "$PTLNX_FOLDER" ]]; then
    echo "$PTLNX_FOLDER created..."
    cd petalinux-tools
else
    echo "Failed to create ${PTLNX_FOLDER}"
    exit 1
fi

PETALINUX_CHMOD_X="$(test -x $PETALINUX_INSTALLER && echo "true" || echo "false")"
# No need to chmod if bit already set
if [[ "${PETALINUX_CHMOD_X}" == "false" ]]; then
    chmod +x ../${PETALINUX_INSTALLER}
    echo -e "\e[33mSetting executable bit for petalinux installer.\n\e[0m"
else
    echo "Installer executable bit already set."
fi

# Shell is currently in petalinux-tools folder.
./../"$PETALINUX_INSTALLER" "$PTLNX_FOLDER"

source ./settings.sh

