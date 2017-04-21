#!/bin/bash
apt-get update
apt-get upgrdae -y
wget http://security.ubuntu.com/ubuntu/pool/main/i/icu/libicu55_55.1-7ubuntu0.1_amd64.deb
dpkg -i dpkg -i libicu55_55.1-7ubuntu0.1_amd64.deb
wget https://github.com/PowerShell/PowerShell/releases/download/v6.0.0-alpha.18/powershell_6.0.0-alpha.18-1ubuntu1.16.04.1_amd64.deb
dpkg -i powershell_6.0.0-alpha.18-1ubuntu1.14.04.1_amd64.deb
apt-get install -f

#standalone powershell binary
#curl -OL https://github.com/PowerShell/PowerShell/releases/download/v6.0.0-alpha.17/PowerShell-x86_64.AppImage
#chmod 777 ./PowerShell-x86_64.AppImage
#./PowerShell-x86_64.AppImage
