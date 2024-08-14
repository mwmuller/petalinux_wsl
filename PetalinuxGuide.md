### Create, Config, Build a project (Manual Steps)
1) To create a project **without** a BSP, run inside ```petalinux-tools```: ```petalinux-create -t project -n <ProjectName> --template zynq```
2) ```cd <ProjectName>```
3) Place your XSA file into ```petalinux_tools``` and run: ```petalinux-config --get-hw-description=../```
   > - ```Subsystem AUTO Hardware Settings``` -> Allows for ps7 cortex configuration. (e.g ethernet, uart, memory addresses etc.)
4) run ```petalinux-config -c kernel``` **This will take some time**
   > - Look for another gui tab to appear (linux-xlnx Configuration) and hit "exit"
5) run ```Petalinux-config -c u-boot```
   > - Look for a second tab to appear on the terminal window (u-boot-xlnx Configuration)
   > - Boot media – enable QSPI Flash and SD/EMMC (two choices) by pressing Y over each of them.
6) Exit and Save
7) Run ```petalinux-config -c rootfs```
   > - From ```apps``` -> Press ```y``` to select ```gpio-demo``` and ```peekpoke```
8) **Optional** If you want to change the tftpboot folder, run ```../../scripts/configure_tftpboot.sh <projectname>```
   * This will update the project specific configuration to copy files to the petalinux-tools/tftpboot folder. 
8) Run ```petalinux-build```
- (this takes awhile ~15 minutes, but if you change a config and build again, it will do incremental builds
and will be faster for successive builds)

### Creating Applications
1) From the project folder, run: ```petalinux-create -t apps -n myapp --enable --template c++```
   * The above example command will create an application called "myapp" in c++
2) New apps can be found: ```<Project>/project-spec/meta-user/recipes-apps/<APPNAME>/files```
   > - New files added will need to be added to the ```<Project>/project-spec/meta-user/recipes-apps/<APPNAME>/<APPNAME>.bb``` files ```SRC_URI``` section
3) Once you've developed your app, you can build it with ```petalinux-build -c myapp```  

### Generating Boot Image (From Project Folder)

1) Once you've built your project, you'll find the ```.elf```/```.bit``` file here: 
> - ```<projectName>/images/linux/*.elf``` (e.g zynq_fsbl.elf)
> - ```<projectName>/images/linux/*.bit```
2) You can run the following command to generate a boot image with your inputs
 > - ```petalinux-package --boot --format BIN --fsbl images/linux/<FSBL ELF FILE>``` <br />
 ``` --u-boot images/linux/<UBOOT ELF FILE>``` <br />
 ``` --fpga images/linux/*.bit --force```
3) This script can be used as well to simplify inputs.
> - ```./../../scripts/generate_boot_image.sh```
> - Use the following args to configure (fsbl/uboot don't require ```.elf```): ```-p <PROJECT NAME> -f <FSBL> -u <UBOOT>```
> - e.g ```./../../scripts/generate_boot_image.sh -p demo -f zynq -u u-boot```
### Full reference guide found here -> [[Reference Guide](https://docs.amd.com/v/u/2019.1-English/ug1144-petalinux-tools-reference-guide)]
