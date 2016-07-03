PROVISION_DIR=/vagrant
HOME_DIR=/home/vagrant

DB_ROOT_PASS=bconf161203

define UBUNTU_MIRRORS
deb mirror://mirrors.ubuntu.com/mirrors.txt trusty main restricted universe multiverse
deb mirror://mirrors.ubuntu.com/mirrors.txt trusty-updates main restricted universe multiverse
deb mirror://mirrors.ubuntu.com/mirrors.txt trusty-backports main restricted universe multiverse
deb mirror://mirrors.ubuntu.com/mirrors.txt trusty-security main restricted universe multiverse
endef

define BASHRC
# Added by provision
export PS1='\[\e]0;\u@\h:\w\a\]\n\[\e[32m\]\u@\h \[\e[33m\]\w\[\e[0m\]\n\$$ '
pushd_v () {
  "pushd" "$$@" > /dev/null && "dirs" -v
}
popd_v () {
  "popd" "$$@" > /dev/null && "dirs" -v
}
alias dirs='dirs -v'
alias popd='popd_v'
alias pushd='pushd_v'
alias la='ls -a'
alias ll='ls -l'
alias lla='ls -la'
alias ls='ls -CF --color=auto --show-control-chars'
endef

define SCREENRC
startup_message off
defencoding UTF-8
#defutf8 on
escape ^Tt
vbell off
defscrollback 1000
termcapinfo xterm 'hs:ts=\E]2;:fs=\007:ds=\E]2;screen\007'
hardstatus string "%?%H %?[screen %n%?: %t%?] %h"
endef

define MYCNF_SYS
[mysqld]
character-set-server = utf8mb4
[mysql]
default-character-set = utf8mb4
[client]
default-character-set = utf8mb4
endef

define MYSQL_SETUP
CREATE DATABASE bconf;
GRANT ALL ON bconf.* TO vagrant@localhost IDENTIFIED BY 'vagrant';
FLUSH PRIVILEGES;
endef

define MYCNF_USER
[mysql]
socket = /var/run/mysqld/mysqld.sock
password = vagrant
database = bconf
endef

define CONFIG_JSON
{
    "DATE_FORMAT": "%Y-%m-%d",
    "DB_INFO": {
        "host": "localhost",
        "db": "bconf",
        "user": "vagrant",
        "passwd": "vagrant"
    },
    "OCTAV": {
        "BASE_URI": "",
        "key": "",
        "secret": ""
    },
    "GITHUB": {
        "client_id": "",
        "client_secret": ""
    }
}
endef

export UBUNTU_MIRRORS
export BASHRC
export SCREENRC
export MYCNF_SYS
export MYSQL_SETUP
export MYCNF_USER
export CONFIG_JSON


default:

ubuntu-all:
	sudo make -f /vagrant/provision.mk ubuntu-root
	sudo -u vagrant -i make -f /vagrant/provision.mk ubuntu-user

ubuntu-root: \
	ubuntu-apt \
	ubuntu-packages \
	ubuntu-mysql \
	ubuntu-pip

ubuntu-user: \
	ubuntu-home \
	ubuntu-dbsetup

ubuntu-apt:
	# Uninstall puppet and chef.
	apt-get remove -y puppet chef
	apt-get autoremove -y
	# Use apt mirrors.
	echo "$$UBUNTU_MIRRORS" | cat - /etc/apt/sources.list > \
		/etc/apt/sources.list.new
	mv /etc/apt/sources.list /etc/apt/sources.list.orig
	mv /etc/apt/sources.list.new /etc/apt/sources.list
	# Update catalog and pre-installed packages.
	apt-get update
	apt-get upgrade -y

ubuntu-packages:
	apt-get install -y libmysqlclient-dev

ubuntu-mysql:
	echo 'mysql-server mysql-server/root_password password ${DB_ROOT_PASS}' | debconf-set-selections
	echo 'mysql-server mysql-server/root_password_again password ${DB_ROOT_PASS}' | debconf-set-selections
	apt-get install -y mysql-server-5.6
	echo "$$MYCNF_SYS" >> /etc/mysql/conf.d/bconf.cnf
	service mysql restart
	echo "$$MYSQL_SETUP" | mysql --password="${DB_ROOT_PASS}"

ubuntu-pip:
	apt-get install -y python3-pip
	pip3 install request bottle mysqlclient

ubuntu-home:
	# Build home directory and configs.
	touch .hushlogin
	ln -s /vagrant vagrant
	echo "$$BASHRC" >> "${HOME_DIR}/.bashrc"
	echo "$$SCREENRC" >> "${HOME_DIR}/.screenrc"
	echo "$$MYCNF_USER" >> "${HOME_DIR}/.my.cnf"
	echo "$$CONFIG_JSON" > "${HOME_DIR}/vagrant/config.json"

ubuntu-dbsetup:
	cd "${HOME_DIR}/vagrant" && python3 db_setup.py
