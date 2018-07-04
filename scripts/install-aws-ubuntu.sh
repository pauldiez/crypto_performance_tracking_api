#!/bin/bash
# install commands for ubuntu 16.04
# disable writing to the history file, while still allowing cycling through the last commands using up/down
echo  'unset HISTFILE' >> ~/.bashrc

#install the latest version of docker
sudo apt-get update -y
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update -y
apt-cache policy docker-ce
sudo apt-get install -y docker-ce
sudo systemctl start docker
sudo systemctl enable docker
sudo service docker start

#install docker compose
sudo curl -L https://github.com/docker/compose/releases/download/1.18.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# grant god mode to users
sudo usermod -a -G docker root
sudo usermod -a -G docker ubuntu

# install make
sudo apt-get install make

#install redis to test connections
sudo apt-get install build-essential tcl -y
cd /tmp
curl -O http://download.redis.io/redis-stable.tar.gz
tar xzvf redis-stable.tar.gz
cd redis-stable
make
sudo make install

# install ansible
sudo apt-add-repository ppa:ansible/ansible -y
sudo apt-get update -y
sudo apt-get install -y ansible








