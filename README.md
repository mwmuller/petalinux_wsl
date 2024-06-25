## WSL/Docker Installation Pre-Requisites **(Must be done first)**
1) Open the wsl-localenv folder to install WSL and Docker


## Petalinux Installer

1) To downlaod the petalinux-installer (if not done so already), go here: https://account.amd.com/en/forms/downloads/xef.html?filename=petalinux-v2019.2-final-installer.run
2) Transfer the downloaded installer to this repo. ```/home/\<username\>\petalinux_wsl```
#
## Setup the Devcontainer
Before you can run the required scripts and tools you'll need to reopen your env in the devcontainer
#
### Note:
    !!!This process needs to be done each time you want to use the devcontainer!!!
1) In the bottom left of vc-code you can click the "><" -> ```Connect to WSL``` -> Select the ```petalinx-wsl``` folder <br />
    - Alternativly ```ctrl + shift + p``` -> ```Connect to WSL```

2) In the bottom left of vc-code you can click the "><" -> ```Dev-container > Reopen in container``` <br />
    - ```ctrl + shift + p``` -> ```Dev-container: Reopen in container```

- To open a new ```bash``` terminal you can use the key-bind ```ctrl + shift + ` ```

## Petalinux setup **(Requires Petalinux-installer)**
1) Run the ```./first-time-ptlnx-setup.sh``` to setup the petalinux environment

**(OPTIONAL)**
- You can include your own ```version``` of petalinux with ```-v```: ```./first-time-ptlnx-setup.sh -v petalinux-v20xx.x-installer.run```
- The default directory for the petalinux installation is ```${WorkingDirectory}/petalinux-tools``` <br />
You can update this with ```-p``` and provide the desired path: ```./first-time-ptlnx-setup.sh -p <newPath>```
### REQUIRED ###
#
There are ```2``` instances during installation where user input is required: 
- Checking Petalinux installer integrity
- Petalinux installation
**Enter ```q``` to exit ```eula.txt``` when it pops up and type ```y```**

### Troubleshooting/Help
1) Here is the link to the 2019.2 Petalinux installation guide: https://docs.amd.com/v/u/2019.2-English/ug1144-petalinux-tools-reference-guide