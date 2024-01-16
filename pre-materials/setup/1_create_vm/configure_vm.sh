#!/bin/bash

# This script performs the following three tasks: 
# 1) randomly pick a floating IP and assign it to a given instance,
# 2) add the given instance to a given security group, 
# 3) lock the given instance to prevent it from being deleted accidentally.

# usage: $./create_user.sh -n <instance_name> -s <security_group_name>
# e.g. $./configure_vm.sh -n luoyumo2-tutorial -s ssh

set -eoau pipefail


function print_help {
  echo ""
  echo "options:"
  echo "  -h Print this help message and exit"
  echo "  -n=INSTANCE_NAME"
  echo "  -s=SECURITY_GROUP"
  echo "  -f=FIXED_IP_ADDRESS"                               
}

while getopts hn:s: flag
do
    case "${flag}" in
        h)
          print_help
          exit 0
        ;;
        n) INSTANCE_NAME=${OPTARG};;
        s) SECURITY_GROUP=${OPTARG};;
        f) FIXED_IP_ADDRESS=${OPTARG}
        *)
          echo 'Error in command line parsing' >&2
          print_help
          exit 1
    esac
done

# get a string of available floating IPs
floating_ip_string=$(openstack floating ip list -f value -c "Floating IP Address" --status DOWN)

# Split the string of IPs into an array
floating_ip_list=()
for ip in $floating_ip_string; do floating_ip_list+=($ip) ; done

# select a random index between 0 and floating_ip_list_length-1 (inclusive)
floating_ip_list_length=${#floating_ip_list[@]}
index=$((RANDOM % floating_ip_list_length))
# use the random index to pick a floating IP
selected_floating_ip=${floating_ip_list[$index]}

# assign floating IP
openstack server add floating ip ${INSTANCE_NAME} ${selected_floating_ip}
echo "floating ip" ${selected_floating_ip} has been assigned to ${INSTANCE_NAME}

# assign security group
string_contain_sg_name=$(openstack server show ${INSTANCE_NAME} -f value -c security_groups)
if [[ "$string_contain_sg_name" == *"$SECURITY_GROUP"* ]]
then
    echo ${INSTANCE_NAME} has already been added to security group ${SECURITY_GROUP}, do nothing 
else
    openstack server add security group ${INSTANCE_NAME} ${SECURITY_GROUP}
    echo added ${INSTANCE_NAME} to security group ${SECURITY_GROUP}
fi

# lock the instance to prevent accidential deletion
openstack server lock ${INSTANCE_NAME}
echo locked ${INSTANCE_NAME} to prevent accidential deletion