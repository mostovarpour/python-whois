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

        # Install Unbound
        yum install -y unbound

        echo "server:
                directory: \"/etc/unbound\"
                username: unbound
                pidfile: \"/etc/unbound/unbound.pid\"
                access-control: 10.0.0.0/8 allow
                access-control: 127.0.0.0/8 allow
                access-control: 192.168.0.0/16 allow
                cache-max-ttl: 14400
                cache-min-ttl: 300
                hide-identity: yes
                hide-version: yes
                interface: 127.0.0.1
                minimal-responses: yes
                num-threads: 4
                prefetch: yes
                qname-minimisation: yes
                rrset-roundrobin: yes
                use-caps-for-id: yes
                verbosity: 1

            forward-zone:
                name: \".\"
                forward-addr: 1.1.1.1        # Cloudflare
                forward-addr: 1.0.0.1        # Cloudflare
                forward-addr: 8.8.4.4        # Google
                forward-addr: 8.8.8.8        # Google
                forward-addr: 37.235.1.174   # FreeDNS
                forward-addr: 37.235.1.177   # FreeDNS
                forward-addr: 50.116.23.211  # OpenNIC
                forward-addr: 64.6.64.6      # Verisign
                forward-addr: 64.6.65.6      # Verisign" > /etc/unbound/unbound.conf

        # enable our test.com zone 
        echo "server: " >> /etc/unbound/unbound.conf
        echo "local-zone: \"test.com\" transparent" >> /etc/unbound/unbound.conf

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
        echo "Successfully added another 100 A records." >&2
        ;;
    m)
        domain="127.0.0.1"
        for ns in $(host -t ns $domain | cut -d" " -f4);do
            host -l $domain $ns | grep "has address" > $domain.txt
            done
            if [ ! -s "$domain.txt" ]; then
                    echo "Zone Transfer Failed!"
                    rm "$domain.txt"
            else
                    echo "Zone Transfer Completed Successfully!"
            fi
        ;;
    \?)
        echo "Invalid option: -$OPTARG" >&2
        ;;
    esac
done
