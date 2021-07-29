#!/bin/bash 

GB='\033[1;32m'
YB='\033[1;33m' 
NC='\033[0m' 

# Install amass 
echo -e "${YB}[*]${NC} Install amass..."
sudo snap install amass  

# Install assetfinder
echo -e "${YB}[*]${NC} Install assetfinder..."
go get -u github.com/tomnomnom/assetfinder

# Install findomain
echo -e "${YB}[*]${NC} Install findomain..."
pushd /tmp
wget https://github.com/Findomain/Findomain/releases/download/4.3.0/findomain-linux
mv findomain-linux findomain
chmod +x findomain
mv findomain /usr/local/bin/
popd  

# Downlaod commonspeak2 wordlist
echo -e "${YB}[*]${NC} Install Downloading commonspeak2 wordlist into '/root/tools/wordlists/commonspeak2.txt'..."
mkdir -p /root/tools/wordlists
wget https://github.com/assetnote/commonspeak2-wordlists/raw/master/subdomains/subdomains.txt -O commonspeak2.txt

# install massdns 
echo -e "${YB}[*]${NC} Install massdns..."
apt install git make gcc -y
pushd /tmp
git clone https://github.com/blechschmidt/massdns.git
cd massdns
make
cp bin/massdns /usr/local/bin/
cd ..
rm -rf massdns
popd

