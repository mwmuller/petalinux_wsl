## WSL/Docker Installation
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
    1a) Alternativly ```ctrl + shift + p``` -> ```Connect to WSL```

2) In the bottom left of vc-code you can click the "><" -> ```Dev-container > Reopen in container``` <br />
    2b) ```ctrl + shift + p``` -> ```Dev-container: Reopen in container```

- To open a new ```bash``` terminal you can use the key-bind ```ctrl + shift + ` ```

## Petalinux setup **(Requires Petalinux-installer)**
1) Run the ```./first-time-ptlnx-setup.sh``` to setup the petalinux environment
    - To include your own version of petalinux, pass the file name as an arg: ```./first-time-ptlnx-setup.sh petalinux-v20xx.x-installer.run```
2) 