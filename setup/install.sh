#!/bin/bash

IFS='/' read -a array <<< pwd

if [[ "$(pwd)" != *setup ]]
then
    cd ./setup
fi

version=$( lsb_release -r | grep -oP "[0-9]+" | head -1 )
if lsb_release -d | grep -q "Fedora"; then
	Release=Fedora
	dnf install -y python-devel m2crypto python-m2ext swig python-iptools python3-iptools libssl-dev
	pip install pycrypto
	pip install iptools
	pip install pydispatcher
	pip install flask
	pip install pyOpenSSL
elif lsb_release -d | grep -q "Kali"; then
	Release=Kali
	apt-get install -y python-dev python-m2crypto swig python-pip libssl-dev
	pip install pycrypto
	pip install iptools
	pip install pydispatcher
	pip install flask
        pip install pyOpenSSL
        if ! which powershell > /dev/null; then
            wget http://security.debian.org/debian-security/pool/updates/main/o/openssl/libssl1.0.0_1.0.1t-1+deb8u6_amd64.deb
            dpkg -i libssl1.0.0_1.0.1t-1+deb8u6_amd64.deb
            wget https://github.com/PowerShell/PowerShell/releases/download/v6.0.0-alpha.16/powershell_6.0.0-alpha.16-1ubuntu1.16.04.1_amd64.deb
            dpkg -i powershell_6.0.0-alpha.16-1ubuntu1.16.04.1_amd64.deb
            apt-get install -f -y
            rm libssl1.0.0_1.0.1t-1+deb8u6_amd64.deb
	    rm powershell_6.0.0-alpha.16-1ubuntu1.16.04.1_amd64.deb
        fi
        cp -r ../lib/powershell/Invoke-Obfuscation /usr/local/share/powershell/Modules
elif lsb_release -d | grep -q "Ubuntu"; then
	Release=Ubuntu
	apt-get install -y python-dev python-m2crypto swig python-pip libssl-dev
	pip install pycrypto
	pip install iptools
	pip install pydispatcher
	pip install flask
	pip install pyOpenSSL
else
	echo "Unknown distro - Debian/Ubuntu Fallback"
	 apt-get install -y python-dev python-m2crypto swig python-pip libssl-dev
	 pip install pycrypto
	 pip install iptools
	 pip install pydispatcher
	 pip install flask
	 pip install pyOpenSSL
fi

# set up the database schema
./setup_database.py

# generate a cert
./cert.sh

cd ..

echo -e '\n [*] Setup complete!\n'
