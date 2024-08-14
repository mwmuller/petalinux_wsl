#!/bin/bash

# configuring the tftpboot folder in devcontainer
echo "Creating tftpboot folder for images..."
mkdir -p ${PETALINUX}/tftpboot

sudo chmod 755 ${PETALINUX}/tftpboot

echo "Updating default folder configuration"

echo "Updating project specifict default tftpboot image folder..."
sed -i 's/^\(CONFIG_SUBSYSTEM_TFTPBOOT_DIR=\).*/\1"tftpboot"/' ${PETALINUX}/$1/project-spec/configs/config

echo "Change complete..."

sudo cat ${PETALINUX}/$1/project-spec/configs/config | grep CONFIG_SUBSYSTEM_TFTPBOOT_DIR