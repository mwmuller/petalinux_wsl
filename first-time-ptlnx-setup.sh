#!/bin/bash
# Ensure SHELL is set to /bin/bash
export SHELL=/bin/bash

# Optionally add /bin/bash to your PATH, if needed
export PATH=/bin/bash:$PATH
# Running the petalinux sh from support.xilinx.com/s/article/73296
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
    echo "$PETALINUX Folder already created do you want to delete it? [y/n]"
    read SELECTION
    if [[ "$SELECTION" == "y" ]]; then
        echo "Removing tools folder"
        rm -rf "$PETALINUX"
    else
        echo "Continuing installing process with non-empty directory..."
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
SKIP_LICENSE=y "$ROOT_DIR"/"$PETALINUX_INSTALLER" "$PETALINUX"


PETALINUX_SETTINGS="$PETALINUX"/settings.sh
SETTINGS_CHMOD_X="$(test -x $PETALINUX_SETTINGS && echo "true" || echo "false")"
# No need to chmod if bit already set
if [[ "${SETTINGS_CHMOD_X}" == "false" ]]; then
    chmod +x ${PETALINUX_SETTINGS}
    echo -e "\e[33mSetting executable bit for settings.sh.\n\e[0m"
else
    echo "Installer executable bit already set."
fi

# export DEBIAN_FRONTEND=dialog
# sudo dpkg-reconfigure dash
source "$PETALINUX_SETTINGS"

