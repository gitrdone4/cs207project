#!bin/bash
clear
echo "Setting up..."

sudo apt-get update

wget http://s3.amazonaws.com/cs207-bucket/cs207_aws_ec2_stack.sh

chmod a+x cs207_aws_ec2_stack.sh

sudo ./cs207_aws_ec2_stack.sh

sudo apt-get install git

cd ~/cs207project
sudo apt-get install python3
sudo apt-get install python3-setuptools

sudo python3 setup.py install

sudo pip3 install scipy
sudo apt-get install python3-portalocker