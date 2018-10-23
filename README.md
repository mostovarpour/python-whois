# A simple WHOIS server written in Python. Runs on CentOS 7 and uses Python, MySQL, and Docker.


### Uses pip to manage python packages.
---

OSX - `brew install pip`

CentOS - `yum install python-pip`

### Install Docker
---
OSX - `brew cask install docker`

CentOS - `sudo yum install docker`

---

### Basic Setup on a CentOS Server
`sudo yum -y update && sudo yum install -y git wget bind-utils tmux python-pip && git clone https://github.com/mostovarpour/python-whois.git`

`wget https://dev.mysql.com/get/mysql80-community-release-el7-1.noarch.rpm`

`sudo rpm -ivh https://dev.mysql.com/get/mysql80-community-release-el7-1.noarch.rpm`

`sudo yum install mysql-server`

If you need to find the root password use this:

`sudo grep 'temporary password' /var/log/mysqld.log`

`sudo systemctl start mysqld`

`sudo pip install pymysql`
