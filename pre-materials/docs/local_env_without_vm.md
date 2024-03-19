# Setting up the local environment without VM
1. Clone the repository (`git clone https://version.helsinki.fi/luoyumo/engineering_of_ml_systems.git`). You will be asked to enter a username and password, these are your university credentials. 
1. Install Anaconda from [its offcicial website](https://docs.anaconda.com/free/anaconda/install/index.html).
1. Set up your conda env. 
```bash
# Under the same directory as this file
conda env create -f mlops_eng_environment.yaml # The YAML file located in the same directory as this doc

# Switch to created conda environment
conda activate mlops_eng
```
Remember to ensure that you are always in the correct Python environment.

4. Install [Ansible](https://docs.ansible.com/ansible/latest/index.html), which is a tool for running commands/scripts in remote machines from your local machine. 
```bash
python3 -m pip install --user ansible
```
5. Install [kubectl (version 1.27.0)](https://kubernetes.io/docs/tasks/tools/#kubectl), which is the tool used to communicate with the K8s cluster.

6. Install jq (for processing JSON) and hey (for generating HTTP loads). These tools will be used later in the course.
```bash
sudo apt install hey jq
```

After finishing the preparation, continue with the "2. Create a VM in cPouta" section in the [main instructions](../README.md#2-create-a-vm-in-cpouta). 