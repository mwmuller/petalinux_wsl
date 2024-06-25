#!/bin/bash

# Running the petalinux sh from support.xilinx.com/s/article/73296
CREATE_INSTALL="true"
ROOT_DIR=$(pwd)
# Default values
PETALINUX_INSTALLER="petalinux-v2019.2-final-installer.run"
PETALINUX="$ROOT_DIR/petalinux-tools"
# Parse command-line options using getopts
while getopts ":v:p:" opt; do
  case ${opt} in
    v ) PETALINUX_INSTALLER=$OPTARG ;;
    p ) PETALINUX=$OPTARG ;;
    \? ) echo "Usage: ./first-time-ptlnx-setup [-i installer] [-p folder]"
      exit 1 ;;
  esac
done

if [[ -d "$PETALINUX" ]]; then
    echo "$PETALINUX Folder alredy created do you want to delete it and re-install? [y/n]"
    read SELECTION
    if [[ "$SELECTION" == "y" ]]; then
        CREATE_INSTALL="true"
        echo "Removing tools folder"
        rm -rf "$PETALINUX"
    else
        echo "Exitting..."
        exit 1
    fi
fi

mkdir ${PETALINUX} 
if [[ -d "$PETALINUX" ]]; then
    echo "$PETALINUX created..."
else
    echo "Failed to create ${PETALINUX}"
    exit 1
fi

PETALINUX_CHMOD_X="$(test -x $PETALINUX_INSTALLER && echo "true" || echo "false")"
# No need to chmod if bit already set
if [[ "${PETALINUX_CHMOD_X}" == "false" ]]; then
    chmod +x $ROOT_DIR/${PETALINUX_INSTALLER}
    echo -e "\e[33mSetting executable bit for petalinux installer.\n\e[0m"
else
    echo "Installer executable bit already set."
fi

# Shell is currently in petalinux-tools folder.
export PETALINUX # export for script env
"$ROOT_DIR"/"$PETALINUX_INSTALLER" "$PETALINUX"

source ./"$PETALINUX"/settings.sh

