#!/usr/bin/env bash

#install ansible - we use this to encrypting are secret variables for production
tput setaf 1
echo "installing ansible..."
tput setaf 15


pip install --trusted-host pypi.python.org pytest-xdist
pip install --trusted-host pypi.python.org --upgrade pip
curl https://bootstrap.pypa.io/get-pip.py | python
sudo pip install ansible
which ansible

# install redis - we will use the 'redis-cli ping' command to test our docker redis server connection
tput setaf 1
echo "installing redis.."
tput setaf 15

mkdir redis && cd redis
curl -O http://download.redis.io/redis-stable.tar.gz
tar xzvf redis-stable.tar.gz
cd redis-stable
make
make test
sudo make install
redis-cli shutdown



#install psql (postgres command line tool) - we will use the 'psql' command to test our docker db server connection
tput setaf 1
echo "installing postgres client... (not the server)"
tput setaf 15

ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew doctor
brew update
brew install libpq
ln -s /usr/local/Cellar/libpq/10.4/bin/psql /usr/local/bin/psql

#install docker (postgres command line tool) - we will use the 'psql' command to test our docker db server connection
tput setaf 1
echo "installing docker"
tput setaf 15

brew cask install docker
brew install bash-completion
brew install docker-completion
brew install docker-compose-completion
brew install docker-machine-completion

