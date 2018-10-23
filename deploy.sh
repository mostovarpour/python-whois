#!/bin/bash

if [[ "$UID" -ne 0 ]]; then
  echo "Sorry, you need to run this as root"
  exit 1
fi

lsof -i :53 > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "It looks like another software is listnening on port 53:"
  echo ""
  lsof -i :53
  echo ""
  echo "Please disable or uninstall it before installing unbound."
  while [[ $CONTINUE != "y" && $CONTINUE != "n" ]]; do
    read -rp "Do you still want to run the script? Unbound might not work... [y/n]: " -e CONTINUE
  done
  if [[ "$CONTINUE" = "n" ]]; then
    exit 2
  fi
fi

if [[ -e /etc/centos-release || -e /etc/redhat-release || -e /etc/system-release && ! -e /etc/fedora-release ]]; then
  OS="centos"
else
  echo "Looks like you aren't running this installer on CentOS"
  exit 3
fi

echo ""
echo "Welcome! This script will install and configure Unbound, and set it as your default system DNS resolver."
echo ""
read -n1 -r -p "Press any key to continue..."
echo ""

if [[ "$OS" = "centos" ]]; then
  # Install Unbound
  yum install -y unbound

  # Configuration
  sed -i 's|# interface: 0.0.0.0$|interface: 127.0.0.1|' /etc/unbound/unbound.conf
  sed -i 's|# hide-identity: no|hide-identity: yes|' /etc/unbound/unbound.conf
  sed -i 's|# hide-version: no|hide-version: yes|' /etc/unbound/unbound.conf
  sed -i 's|use-caps-for-id: no|use-caps-for-id: yes|' /etc/unbound/unbound.conf
fi

if [[ ! "$OS" =~ (fedora|centos) ]];then
  # DNS Rebinding fix
  echo "private-address: 10.0.0.0/8
private-address: 172.16.0.0/12
private-address: 192.168.0.0/16
private-address: 169.254.0.0/16
private-address: fd00::/8
private-address: fe80::/10
private-address: 127.0.0.0/8
private-address: ::ffff:0:0/96" >> /etc/unbound/unbound.conf
fi

if pgrep systemd-journal; then
  systemctl enable unbound
  systemctl restart unbound
else
  service unbound restart
fi

# Allow the modification of the file
chattr -i /etc/resolv.conf

# Disable previous DNS servers
sed -i "s|nameserver|#nameserver|" /etc/resolv.conf
sed -i "s|search|#search|" /etc/resolv.conf

# Set localhost as the DNS resolver
echo "nameserver 127.0.0.1" >> /etc/resolv.conf

# Disallow the modification to prevent the file from being overwritten by the system.
# Use -i to enable modifications
chattr +i /etc/resolv.conf

echo "The installation is done."