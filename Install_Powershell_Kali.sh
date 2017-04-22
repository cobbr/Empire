#!/bin/bash
apt-get update
apt-get upgrade -y
wget http://security.ubuntu.com/ubuntu/pool/main/i/icu/libicu55_55.1-7ubuntu0.1_amd64.deb
dpkg -i dpkg -i libicu55_55.1-7ubuntu0.1_amd64.deb
apt-get install -f
wget http://security.debian.org/debian-security/pool/updates/main/o/openssl/libssl1.0.0_1.0.1t-1+deb7u2_amd64.deb
dpkg -i libssl1.0.0_1.0.1t-1+deb7u2_i386.deb
apt-get install -f
wget https://github.com/PowerShell/PowerShell/releases/download/v6.0.0-alpha.18/powershell_6.0.0-alpha.18-1ubuntu1.16.04.1_amd64.deb
dpkg -i powershell_6.0.0-alpha.18-1ubuntu1.14.04.1_amd64.deb
apt-get install -f
rm powershell_6.0.0-alpha.18-1ubuntu1.14.04.1_amd64.deb
rm libicu55_55.1-7ubuntu0.1_amd64.deb

#standalone powershell binary
#curl -OL https://github.com/PowerShell/PowerShell/releases/download/v6.0.0-alpha.17/PowerShell-x86_64.AppImage
#chmod 777 ./PowerShell-x86_64.AppImage
#./PowerShell-x86_64.AppImage
