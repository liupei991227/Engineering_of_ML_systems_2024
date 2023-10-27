# Using QEMU for setting up a local virtual machine

If you have troubles installing VirtualBox in your Linux machine, you can use QEMU as the virtualization tool. 

**Note**: You need sudo rights for this. For Cubbli users: 

If you have a fuxi laptop, you can activate them with a command: `i-want-sudo-access`.

If you do not have them or do not want them, turn on Remote Help from HY-menu (top corner of the screen), copy your computers info from the pop up, contact cubbli-admin@helsinki.fi with a header

"MLOps setup virtualization"

and as a message:
```text
I need urgent help with setting up virtual environment for the course Engineering of Machine Learning Systems,
and I do not have sudo access.

1. Install cubbli-kvm

apt install cubbli-kvm


2. Add me to libvirt group:

usermod -aG libvirt [YOUR USERNAME]


Computer info:
[COMPUTER INFO FROM POP UP]
```

Our team will watch closely for requests during office hours.
If we miss the window when you are online, send a message for when would be a suitable time.

---

If you have sudo rights, you can follow the following 

## Prepare local host

First, install the required dependencies.
When you read these, they might already be installed.
```bash
sudo apt virt-manager ovmf qemu-kvm libvirt-daemon qemu-kvm
```

On Cubbli, these are in a package named cubbli-kvm
and you can install it with:
```bash
sudo apt install cubbli-kvm
```

After that, add yourself to the virtualization user group:
```bash
sudo addgroup $USER libvirt
```

You should logout and login at this point to refresh your groups.


## Prepare the file

Download the OVA file. An OVA file is basically an archive of various files associated with a VM. Open the archive:
```bash
tar xf mlops-eng.ova
```

Convert the disk image to suitable format
```bash
qemu-img convert mlops-eng-disk001.vmdk mlops-eng-disk001.qcow2
```

## Prepare virtual machine

Create a volume for virtual machine images
```bash
virsh pool-create-as --name libvirt-home --type dir --target "/home/libvirt-home"
```
(If you are on a non-cubbli machine, you have to create the directory first)

Move the disk image from this directory to libvirt's directory
```bash
mv mlops-eng-disk001.qcow2 /home/libvirt-home/
```

Open Virtual Machine Manager (running `virt-manager` in your console).

From File-menu (top-left corner), Add Connection. Use default (QEMU/KVM) and Connect.

Right-click QEMU/KVM-connection -> select "New" -> Import existing disk image.

Browse -> Select "mlops-eng-disk001.qcow2" from libvirt-home volume -> Choose Volume 

If you don't see it, press "Refresh Volume list" (the small circular arrow).

Select Ubuntu 22.04 as operating system -> Forward

Assign 10633 MB of memory and 4 cores to your VM. All other settings can be default

Your virtual machine is now ready to use.

Install qemu-guest-agent on virtual machine for greater control of it:
```bash
sudo apt install qemu-guest-agent
```

If you have troubles using it, please post your issues in the Moodle forum.

If you have troubles setting it up, please contact cubbli-admin@helsinki.fi

---
After you've prepared your local VM, you can go back to the [main instructions](../README.md#5-log-in-to-the-virtual-machine). 