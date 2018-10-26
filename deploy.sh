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
        echo "Please disable or uninstall it before installing bind."
        while [[ $CONTINUE != "y" && $CONTINUE != "n" ]]; do
            read -rp "Do you still want to run the script? bind might not work... [y/n]: " -e CONTINUE
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

        # Install bind
        yum install -y bind bind-utils

        # copy the config file
        cp /etc/named.conf /etc/named.conf.orig

        # set up /etc/named.conf
        echo "options {
                    #listen-on port 53 { 127.0.0.1; };
                    listen-on-v6 port 53 { ::1; };
                    directory	\"/var/named\";
                    dump-file	\"/var/named/data/cache_dump.db\";
                    statistics-file \"/var/named/data/named_stats.txt\";
                    memstatistics-file \"/var/named/data/named_mem_stats.txt\";
                    allow-query { any; };
                    allow-transfer     { localhost; };
                    recursion yes;

                    dnssec-enable yes;
                    dnssec-validation yes;
                    dnssec-lookaside auto;

                    /* Path to ISC DLV key */
                    bindkeys-file \"/etc/named.iscdlv.key\";

                    managed-keys-directory \"/var/named/dynamic\";
            };" > /etc/named.conf
        
        echo "zone \"test.com\" IN {
                type master;
                file \"test.com.zone\";
                allow-update { none; };
        };" >> /etc/named.conf

        # set up our test.com zone file
        echo "\$TTL 86400
@   IN  SOA     test.com. root.test.com. (
2013042201  ;Serial
3600        ;Refresh
1800        ;Retry
604800      ;Expire
86400       ;Minimum TTL
)
; Specify our two nameservers
IN	NS		ns1.test.com.
IN	NS		ns2.test.com.
; Resolve nameserver hostnames to IP, replace with your two droplet IP addresses.
ns1		IN	A		127.0.0.1
ns2		IN	A		127.0.0.1

; Define hostname -> IP pairs which you wish to resolve
@		IN	NS		localhost.
@		IN	A		127.0.0.1
www		IN	A		127.0.0.1" > /var/named/test.com.zone

        #Add the 1000 A records
        for i in `seq 1 1000`; do
            echo "r"$i"		IN	A		127.0.0.1" >> /var/named/test.com.zone
        done

        if pgrep systemd-journal; then
        systemctl enable named
        systemctl restart named
        else
        service named restart
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
        if [ -e /var/named/test.com.zone ]; then
            #Add the 100 A records if the -u flag was given
            last=`awk '/./{line=$0} END{print line}' /var/named/test.com.zone | cut -f1 | sed 's/r//'`
            last=$((last+1))
            lastplus=$((last+100))
            for i in `seq $last $lastplus`; do
                echo "r"$i"		IN	A		127.0.0.1" >> /var/named/test.com.zone
            done
            echo "Successfully added another 100 A records." >&2

            if pgrep systemd-journal; then
            systemctl restart named
            else
            service named restart
            fi
        else
            echo "Please run the script with the -i option first."
        fi
        ;;
    m)
        if [ -e /var/named/test.com.zone ]; then
            domain="test.com"
            # if domain.txt exists then copy it for the comparison
            if [ -e $domain.txt ]; then
                cp $domain.txt $domain.txt-compare
            fi

            # perform the zone transfer
            for ns in $(host -t ns $domain | cut -d" " -f4);do
                host -l $domain $ns | grep "has address" > $domain.txt
                done
                if [ ! -s "$domain.txt" ]; then
                        echo "Zone Transfer Failed!"
                        rm "$domain.txt"
                else
                        echo "Zone Transfer Completed Successfully!"

                fi
            # start the comparison
            if [ -e $domain.txt-compare ]; then
                file1=(`md5sum $domain.txt`)
                file2=(`md5sum $domain.txt-compare`)
                if [ "$file1" != "$file2" ]; then
                    echo "Zone file has changed!" >&2
                else
                    echo "Zone file has not changed." >&2
                fi
            fi
        else
            echo "Please run the script with the -i option first."
        fi
        ;;
    \?)
        echo "Invalid option: -$OPTARG" >&2
        ;;
    esac
done
