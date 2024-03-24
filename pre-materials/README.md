# ML Engineering Course
* Before getting started
    * [An overview of the course environment](#an-overview-of-the-course-environment)
    * [Apply access to CSC](#apply-access-to-csc)
* [Set up the course environment](#set-up-the-course-environment)
    * [Configure your local environment](#1-configure-your-local-environment)
    * [Create a VM in cPouta](#2-create-a-vm-in-cpouta)
    * [Install tools and create a K8s cluster in your cPouta VM](#3-install-necessary-tools-and-create-a-k8s-cluster-in-the-cpouta-vm)
    * [Deploy the MLOps platform](#4-deploy-the-mlops-platform)
    * [Post-configuration](#5-still-a-bit-more-configurations-in-your-local-environment)

**Note**: You'll see two terms "MLOps" and "MLOps platform" appear multiple times in the following instructions. MLOps stands for machine learning operations. From a high level, it's a set of practices that streamline the processes of training, deploying, and monitoring models. MLOps platform is a software platform that offer different components (tools and services) to let you practice MLOps. You'll learn more about MLOps as the course progresses.

## An overview of the course environment
The figure below illustrates the course environment:

![](./docs/images/course_env.jpg)

From a high level, the course environment consists of two parts:
1) An MLOps platform deployed to a Kubernetes cluster running in a remote virtual machine (VM).
2) A local environment with necessary packages installed for communicating with the remote MLOps platform.

First, let's take a glance at Kubernetes, or shortly, K8s (as there are 8 characters between "K" and "s"). K8s is a commonly used technique to deploy and manage containers. If the concept of container is new, you can see it as a "lightweight VM" that contains everything to run an application, including the code, libraries, dependencies, and runtime environment. If we go back to the above figure of the course environment, the MLOps platform actually consists of multiple containers:

![](./docs/images/course_env_container.jpg)

There are two reasons for using this environment in the course:
1) Some of the MLOps platform components are K8s-based. In other words, a K8s cluster is needed to host some services/tools you will use in this course. A K8s cluster is memory demanding. By using a remote virtual machine to run it, you don't need to worry about the memory limitation of your own computer.  
2) This environment can simulate real-world working conditions where a remote platform with extensive computational resources is used to train and deploy  ML models, rather than running everything solely on a local machine with limited memory and CPU/GPU resources.

## Apply access to CSC
As mentioned above, the course environment contains an MLOps platform running in a remote VM. You'll create the remote VM using the cloud service (named cPouta) provided by CSC, known as the Finnish IT center for science. To use CSC, please first apply for the access to it following the link provided on Moodle. 

Please note the following:
- It may take a few days for your application to get approved.
- During the application process, you'll be asked to create a CSC account. **Please start your password with a normal English character (not special characters like !#%&)** to avoid potential issues in the next step where you'll run some code to create a VM in CSC. 
- After you get the confirmation that you have been added to the CSC project used by the course, Please go to [https://my.csc.fi](https://my.csc.fi/dashboard) -> Click "Projects" in the left panel -> Click the "Engineering of ML systems course" project -> Agree to the general terms & conditions of cPouta as shown below.
<img src="./docs/images/cpouta-terms.png" width=300 />


## Set up the course environment
**Warning**: It may take up to a few hours to finish the environment setup, so remember to reserve enough time for this part. 

***If you encounter issues during the setup, please first check if your issues are covered in the [common Q&A](./docs/Q&A.md).***

The instructions below guide you how to set up the course environment. The instructions are based on Linux operating system. 

### 1. Configure your local environment
#### If you're using Linux or macOS...
You can use your host system to set up your local environment as described [here](./docs/local_env_without_vm.md). (The commands in the instruction are based on Linux, feel free to adapt them to fit your need if you're using macOS.)

#### If you're using Windows
- You can install WSL and then follow the [same instruction](./docs/local_env_without_vm.md) for Linux/maxOS users above.
- Another option is to use a pre-built image to create Ubuntu VM following [this instruction for using VM](./docs/local_env_vm.md). 


### 2. Create a VM in cPouta
Now, it is time to start set up the remote MLOps platform. In the instructions below, you will need to run some commands in a terminal. You should run them in your local environment unless separately specified.

**Note**: If you are using the Ubuntu VM in VirtualBox, then the **VM running in VirtualBox (not your host system)** is your local environment. 

In this instruction, you will need to run a Jupyter notebook and commands in a terminal. Using VS Code will make it easier as you can open a terminal in the same VS Code window (Terminal -> New Terminal in the navigation bar) to avoid switching between VS Code and a terminal. 

Go to the setup directory
```bash
cd setup
```
Then follow the instructions in [1_create_vm/openstack.ipynb](./setup/1_create_vm/openstack.ipynb) to launch a VM in cPouta, the IaaS cloud service at CSC (Finnish IT center for science).


### 3. Install necessary tools and create a K8s cluster in the cPouta VM
**Note**: In this and and next part, you'll need to run some scripts in your local environment and the remote cPouta VM. In case you get an error when running the scripts, please first check if your issue is covered [here](./docs/Q&A.md#setting-up-the-mlops-platform-in-cpouta). If not, please pose your issue in the Moodle forum. 

You will use some Ansible scripts to create a K8s cluster in your VM. Simply speaking, Ansible is a tool for running commands/scripts in remote machines from your local machine. 

First, you need to change some configuration so that Ansible knows how to reach your remote VM.

First, Change the `floating_ip` and `ssh_key_file` variables in the [setup/2_ansible_scripts/inventory.ini file](./setup/2_ansible_scripts/inventory.ini) directory:
```
[openstack_vms]
<floating-ip-of-your-vm> ansible_user=ubuntu ansible_ssh_private_key_file=<the-ssh-private-key-file-for-connecting-to-your-vm>
```
You can find the floating_ip and your ssh key file at the end of [1_create_vm/openstack.ipynb](./setup/1_create_vm/openstack.ipynb):

![](./docs/images/ssh_file_and_floating_ip.jpg)

Then run the Ansible scripts
```bash
# Go to the 2_ansible_scripts directory
cd setup/2_ansible_scripts

# Under the 2_ansible_scripts directory
ansible-playbook -i inventory.ini playbook.yaml -vv
```
>In case you are interested, the Ansible scripts will mainly perform two tasks:
>- Install the necessary packages for creating a K8s cluster and deploying the MLOps platform, e.g., Python3, Docker, and [Kind](https://kind.sigs.K8s.io/).
>- Create a K8s cluster and copy the cluster configuration file of the cluster back to your local machine so that you can access the cluster from your local machine. 

It will take some time to finish the execution of the Ansible scripts. If you see the following output, the Ansible scripts have been successfully completed.
```text
PLAY RECAP *********************************************************************
128.214.252.130            : ok=18   changed=13   unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

After running the Ansible scripts, a K8s cluster has been created in your remote cPouta VM. A file named `mlops_config` has been copied to a directory called `.kube` under your home directory in your local machine. This `mlops_config` file includes the information and credentials needed by kubectl (K8s command line tool) to communicate with the K8s cluster. 

Finally, you need to do some configurations so that kubectl in your local environment knows how to access the information and credentials for communicating with your K8s cluster created in your remote cPouta VM.
* Case 1: If you don't have any other K8s cluster running, rename the `mlops_config` file to `config` using the following command. 
```bash
mv ~/.kube/mlops_config ~/.kube/config
```
kubectl will automatically grab the needed credentials from the `config` file.
* Case 2: If you have another K8s cluster running, adjust an environmental variable called `KUBECONFIG` so that kubectl knows that it should access the `mlops_config` file when being executed. 
```bash
# Persist the KUBECONFIG environmental variable
# You only need to run this command once
echo "export KUBECONFIG=~/.kube/mlops_config" >> ~/.bashrc
source ~/.bashrc

# Alternatively, you can mark the variable on the fly, but you need to do this every time you run kubectl in a new terminal session
export KUBECONFIG=~/.kube/mlops_config
```

Make sure kubectl is connecting to the correct cluster
```bash
kubectl config use-context kind-kind-ep
```
Now you should be able to access your K8s cluster from your local machine.
```bash
kubectl get nodes

#You should see one control plane and two worker nodes 
NAME                    STATUS   ROLES           AGE   VERSION
kind-ep-control-plane   Ready    control-plane   16m   v1.24.0
kind-ep-worker          Ready    <none>          16m   v1.24.0
kind-ep-worker2         Ready    <none>          16m   v1.24.0
```
#### Back up K8s cluster credentials if you're using a Ubuntu VM as your local environment
We recommend copying the credentials to somewhere else than your VM. This way, you can access your cluster if you lose access to your VM. You can see the content by 
```bash
cat ~/.kube/config
```
### 4. Deploy the MLOps platform
First you need to access your VM:
```bash
# access your VM
ssh -i <your-ssh-key-file> ubuntu@<floating-ip>
```
The command can be copied from the end of 1_create_vm/openstack.ipynb

![](./docs/images/shell_in_vm.png)

Then run the following commands in your **remote cPouta VM** (not your local machine)
```bash
cd install_platform
# Install the MLOps platform, it will take ~6min to finish the script
./install.sh
```
If you see the following output, the installation has been completed successfully. 
```text
+ echo Installation 'completed!'
Installation completed!
+ echo
+ exit 0
```

Finally, test that MLOps platform is correctly installed
```bash
./scripts/run_tests.sh
```
If you see the following output, all tests have been passed.
```text
================= 38 passed, 20 warnings in 226.05s (0:03:46) ==================
+ exit 0
```

### 5. Still a bit more configurations in your local environment
#### Configure kubectl to access the correct cluster
In your local environment (not the remote cPouta VM), run the following command to make sure you can access your K8s cluster using kubectl:
```bash
# Check which cluster kubectl accesses
kubectl config current-context

# If the output of the command above is not "kind-kind-ep", configure kubectl to access the correct cluster
kubectl config use-context kind-kind-ep
```


#### Configure /etc/hosts 
As previously mentioned, the MLOps platform you just deployed provides different services that facilitate different phases in MLOps. You'll need to access these services during the course using their host names. To enable your local environment knows how to resolve these host names into IP addresses, you need to modify the `/etc/hosts` file.

Please add the following entries to `/etc/hosts`
```text
<floating-IP-of-cPouta-VM> kserve-gateway.local
<floating-IP-of-cPouta-VM> ml-pipeline-ui.local
<floating-IP-of-cPouta-VM> mlflow-server.local
<floating-IP-of-cPouta-VM> mlflow-minio-ui.local
<floating-IP-of-cPouta-VM> mlflow-minio.local
<floating-IP-of-cPouta-VM> prometheus-server.local
<floating-IP-of-cPouta-VM> grafana-server.local
<floating-IP-of-cPouta-VM> evidently-monitor-ui.local
```

Now your local environment knows that it should resolve the host names of the services provided by the MLOps platform into the IP of your cPouta VM where the MLOps platform is running. 

You can use the following command to check if you've configured your `etc/hosts` file correctly:
```bash
# Make sure you're using the mlops_eng conda environment
conda activate mlops_eng

# Suppose you're under the same directory as this file, run the test 
# and you should see one test pass. 
pytest setup/test_remote_connection.py
```
If you see an error like below, please re-check your `etc/hosts` file.
```text
requests.exceptions.ConnectionError: HTTPConnectionPool(host='...', port=80): Max retries exceeded with url: / (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7ccaf102b1d0>: Failed to establish a new connection: [Errno -2] Name or service not known'))
``` 

Now, for example, if you go to [http://mlflow-server.local](http://mlflow-server.local), you should see a Web page similar to the following:

<img src="./docs/images/mlflow-ui.png" width=800/>

#### If you're using VS code...
You probably have the Pylance extension installed. Please make sure the version of your Pylance extension is 2023.5.40 or earlier as the newer versions have some issues with Jupyter Notebook, which makes running Jupyter Notebook in VS Code super slow. You can check your Pylance version in the following steps: open the extension list using ctrl+shift+x -> search Pylance in the search bar and check the version. 

<img src="./docs/images/pylance-version.png" width=500 />

You can downgrade the Pylance version by clicking the down arrow next to the "Uninstall" button and clicking the "Install Another Version" option. You need to reload VS Code after downgrading the Pylance version. 


## Wrap up
After following the instructions, you've set up the course environment, You've deployed the MLOps platform to a remote VM in cPouta. You've also configured your local environment so that you can access the remote MLOps platform from your local environment. 

Though the course environment is based on K8s, no prior knowledge of K8s is needed to complete this course. You won't need to deal with K8s in most of the assignments but can directly use the services/tools provided by the MLOps platform. An exception is week4, where you'll need to deploy some models to the K8s cluster. To prepare you for the assiginments of that specific week, we recommend reviewing [this material](./docker_and_k8s/README.md) if containers and K8s are completely new to you. This will help you gain some basic understanding of the concepts of containers and K8s, ensuring smoother learning experience in the course. 

