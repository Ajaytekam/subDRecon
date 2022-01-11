#!/bin/bash 

GB='\033[1;32m'
YB='\033[1;33m'
NC='\033[0m' 

## update the system 
echo -e "${YB}[*]${NC} Update the system..."
apt update -y 

## install some system tools 
echo -e "${YB}[*]${NC} Install tools..."
apt install vim curl wget git unzip tmux parallel -y

## install python, go
echo -e "${YB}[*]${NC} Install python environments..."
apt install python3.9 python3-pip -y
pip3 install virtualenv  

# install golang
# current version go1.17.6.linux-amd64.tar.gz
echo -e "${YB}[*]${NC} Install golang binaries..."
curl -sSL https://dl.google.com/go/go1.17.6.linux-amd64.tar.gz -o go1.17.6.linux-amd64.tar.gz
tar -C /usr/local -xzf go1.17.6.linux-amd64.tar.gz
rm go1.17.6.linux-amd64.tar.gz
echo "export GOROOT=/usr/local/go" >> ~/.bashrc
echo "export GOPATH=\$HOME/go" >> ~/.bashrc 
echo "export PATH=\$GOPATH/bin:\$GOROOT/bin:\$PATH" >> ~/.bashrc

# message 
echo -e "${YB}[*]${NC} Installation completed..."
echo -e "${YB}[#]${NC} Now run Command \"${GB}source ~/.bashrc${NC}\"..."

