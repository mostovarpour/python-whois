#!/bin/bash

while getopts ":i :u :m" opt; do
  case $opt in
    i)
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

        # Install Unbound
        yum install -y unbound

echo "server:
    directory: \"/etc/unbound\"
    username: unbound
    # make sure unbound can access entropy from inside the chroot.
    # e.g. on linux the use these commands (on BSD, devfs(8) is used):
    #      mount --bind -n /dev/random /etc/unbound/dev/random
    # and  mount --bind -n /dev/log /etc/unbound/dev/log
    chroot: \"/etc/unbound\"
    # logfile: \"/etc/unbound/unbound.log\"  #uncomment to use logfile.
    pidfile: \"/etc/unbound/unbound.pid\"
    # verbosity: 1        # uncomment and increase to get more logging.
    # listen on all interfaces, answer queries from the local subnet.
    interface: 127.0.0.1
    access-control: 10.0.0.0/8 allow
    access-control: 2001:DB8::/64 allow" > /etc/unbound/unbound.conf

        # Configuration
        # sed -i 's|# interface: 0.0.0.0$|interface: 127.0.0.1|' /etc/unbound/unbound.conf
        # sed -i 's|# hide-identity: no|hide-identity: yes|' /etc/unbound/unbound.conf
        # sed -i 's|# hide-version: no|hide-version: yes|' /etc/unbound/unbound.conf
        # sed -i 's|use-caps-for-id: no|use-caps-for-id: yes|' /etc/unbound/unbound.conf

        # enable our test.com zone 
        echo "# Custom test.com zone configured below" >> /etc/unbound/unbound.conf
        echo "local-zone: \"test.com\" static" >> /etc/unbound/unbound.conf

        #Add the 1000 A records
        echo "local-data: \"test.com. IN A 127.0.0.1\"" >> /etc/unbound/unbound.conf
        for i in `seq 1 1000`; do
            echo "local-data: \"r"$i".test.com. IN A 127.0.0.1\"" >> /etc/unbound/unbound.conf
        done

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
      ;;
    u)
        #Add the 100 A records if the -u flag was given
        for i in `seq 1001 1100`; do
            echo "local-data: \"r"$i".test.com. IN A 127.0.0.1\"" >> /etc/unbound/unbound.conf
        done
      ;;
    m)
      echo "-m was triggered!" >&2
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done
