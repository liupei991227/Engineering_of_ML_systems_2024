# Create a new VM as the local environment from scratch
## 1. Launch a VM using Ubuntu 22.04 LTS ISO
- The Ubuntu 22.04 LTS ISO can be downloaded [here](https://ubuntu.com/download/desktop).
- You may want to check the "Skip Unattended Installation" option when creating a new VM, otherwise you may not be able to open a console in your VM. (This is what happened when testing in a Ubuntu host. If you have experience of creating Ubuntu VM and know this won't happen to you, feel free to skip it.)
- Assign ~10GB RAM, 4CPUs, and ~80GB disk space to your VM.
- Use **user** as the username and **password** the password.

## 2. Install packages
```bash
sudo apt update
sudo apt install gcc make perl git curl hey jq
```

## 3. Install guest additions
> Note: If you used the unattended installation, guest additions are already installed and you can skip the rest of this section. 

After launching your VM, you may need to install guest additions, which allow you to make your VM full screen and enable copy-paste between your host system and VM. Click "Devices" in the menu bar on top of the VirtualBox window, then "Insert guest addition CD image". 
```bash
cd /media/user/VBox_GAs_7.0.8/
sudo ./VBoxLinuxAdditions.run
```

## 4. Install other tools needed in the course and prepare the python environment.
Clone the "engineering_of_ml_systems" repository, and install Anaconda, kubectl, and Ansible. See [here](../docs/preparation_without_vm.md).
