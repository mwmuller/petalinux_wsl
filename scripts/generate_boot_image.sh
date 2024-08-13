#!/bin/bash

# pass in the location of the project and find the files
FSBL=""
UBOOT=""
PROJECT="demo"
ROOT_DIR=$(git rev-parse --show-toplevel)
PETA_BUILD_DIR="/images/linux/"
help(){
    echo -e "\t-h   : help functions"
    echo -e "\t-p   : project name used to generate boot image" 
    echo -e "\t-f   : fsbl elf file input"
    echo -e "\t-u   : u-boot elf file input"
    exit 1
}

while getopts "hp:f:u:" arg; do
  case $arg in
    p) 
        PROJECT=${OPTARG} ;;
    f)
        FSBL=${OPTARG} ;;
    u)
        UBOOT=${OPTARG} ;;
  esac
done
BUILD_DIR="${PETALINUX}/${PROJECT}"
if [[ -d "${BUILD_DIR}" ]]; then
    cd ${BUILD_DIR}
    petalinux-package --boot --format BIN --fsbl images/linux/${FSBL}*.elf \
    --u-boot images/linux/${UBOOT}*.elf --fpga images/linux/*.bit --force
else
    echo "Build folder is missing"
fi
