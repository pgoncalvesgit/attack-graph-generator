#!/bin/bash
# Checking if python is installed.
if [ $(which python3) ]; then
     echo "Python3.6 is installed."
else
     echo "Python3.6 is not installed."
     sudo apt-get -y update
     sudo apt-get -y install python3.6
     sudo apt-get -y sudo update-alternatives --config python
     sudo update-alternatives --config python
     sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.6 2
     sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 2
fi



#Check if pip3 is installed
if [ $(which pip3) ]; then
     echo "Pip3 is installed."
else
     echo "Pip3 is not installed."
     sudo apt-get -y install python3-pip
fi



# Checking if docker is installed.
if [ $(which docker) ]; then
     echo "Docker is installed."
else
     echo "Docker is not installed."
     sudo apt-get -y install apt-transport-https ca-certificates curl software-properties-common
     curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
     sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu xenial stable"
     sudo apt-get -y update
     apt-cache search docker-ce
     sudo apt-get -y install docker-ce
fi



# Checking if docker-compose is installed.
if [ $(which docker-compose) ]; then
     echo "Docker-compose is installed."
else
     echo "Docker-compose is not installed."
     sudo curl -L https://github.com/docker/compose/releases/download/1.18.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
     sudo chmod +x /usr/local/bin/docker-compose
fi



# Checking if go is installed.
#GOPATH="/usr/local/go"
if [ -d "$GOPATH" ]; then
  # Control will enter here if $DIRECTORY exists.
   echo "Go is installed."
else
   echo "Go is not installed. Installing go..."
   wget https://golang.org/dl/go1.17.3.linux-amd64.tar.gz
   sudo tar -C /usr/local -xzf go1.17.3.linux-amd64.tar.gz
   rm go1.17.3.linux-amd64.tar.gz
fi
sudo chmod -R 777 "/usr/local/go"



# Checking if GOPATH is set
if [ -d "$GOPATH" ]; then
     echo "GOPATH is already set."
else
     echo "GOPATH is not set. Setting GOPATH..."
     export PATH=$PATH:/usr/local/go/bin
     export GOPATH=/usr/local/go/bin
fi



# Checking if clairctl is installed.
CLAIR_CTL_PATH="/usr/local/go/bin/src/github.com/jgsqware/clairctl"
if [ -d "$CLAIR_CTL_PATH" ]; then
  # Control will enter here if $DIRECTORY exists.
   echo "Clairctl exists."
else
   echo "Clairctl does not exist. Please set up clairctl."

   # Creating needed hierarchy for clairctl.
   if [ ! -d $GOPATH/src/github.com/jgsqware/clairctl ]; then
       echo "Entered here"
       mkdir -p -m 777 $GOPATH/src;
       mkdir -p -m 777 $GOPATH/src/github.com;
       mkdir -p -m 777 $GOPATH/src/github.com/jgsqware;
   fi

   wget https://github.com/jgsqware/clairctl/archive/master.zip
   unzip master.zip -d $GOPATH/src/github.com/jgsqware
   rm master.zip
   mv $GOPATH/src/github.com/jgsqware/clairctl-master $GOPATH/src/github.com/jgsqware/clairctl
fi



# Checking if graphviz is installed
python3 -c "import graphviz" &> /dev/null
if [ "$?" = "1" ]; then
    echo "Graphviz has not been installed. Installing Graphviz..."
    sudo python3 -m pip install graphviz
else
    echo "Graphviz is installed."
fi
if [ $(dpkg-query -W -f='${Status}' graphviz 2>/dev/null | grep -c "ok installed") -eq 0 ]; then
    sudo apt-get -y install graphviz
fi



# Checking if yaml is installed
python3 -c "import yaml" &> /dev/null
if [ "$?" = "1" ]; then
    echo "Pyyaml has not been installed. Installing Pyyaml..."
    sudo python3 -m pip install pyyaml
else
    echo "Pyyaml is installed."
fi



# Checking if networkx is installed
python3 -c "import networkx" &> /dev/null
if [ "$?" = "1" ]; then
    echo "Networkx has not been installed. Installing Networkx..."
    sudo python3 -m pip install networkx
else
    echo "Networkx is installed."
fi



# Checking if numpy is installed
python3 -c "import numpy" &> /dev/null
if [ "$?" = "1" ]; then
    echo "Numpy has not been installed. Installing Numpy..."
    sudo python3 -m pip install numpy
else
    echo "Numpy is installed."
fi




# Checking if unzip is installed
if [ $(which unzip) ]; then
     echo "unzip is installed."
else
     echo "unzip is not installed."
     sudo apt-get -y install unzip
fi




