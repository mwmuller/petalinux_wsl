### Creating a project (Manual Steps)
1) To create a project **without** a BSP, run inside ```petalinux-tools```: ```petalinux-create –t project -n <ProjectName> –-template zynq```
2) ```cd LinuxDemo```
3) Place your XSA file into ```petalinux_tools``` and run: ```petalinux-config –get-hw-description=../```
4) run ```petalinux-config -c kernel``` **This will take some time**
   > - Look for a second tab to appear on the terminal window (linux-xlnx Configuration) and hit "exit"
5) run ```Petalinux-config -c u-boot```
   > - Look for a second tab to appear on the terminal window (u-boot-xlnx Configuration)
   > - Boot media – enable QSPI Flash and SD/EMMC (two choices) by pressing Y over each of them.
6) Exit and Save
7) Run ```petalinux-config -c rootfs```
- Apps – enable gpio-demo and peekpoke. Exit and Save
- ```petalinux-build```
- (this takes awhile ~15 minutes, but if you change a config and build again, it will do incremental builds
and will be faster for successive builds)
