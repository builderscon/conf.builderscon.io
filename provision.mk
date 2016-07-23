PROVISION_DIR=/vagrant
HOME_DIR=/home/vagrant

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

define CONFIG_JSON
{
    "DATE_FORMAT": "%Y-%m-%d",
    "OCTAV": {
        "endpoint": "",
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
export MYCNF_USER
export CONFIG_JSON


default:

ubuntu-all:
	sudo make -f /vagrant/provision.mk ubuntu-root
	sudo -u vagrant -i make -f /vagrant/provision.mk ubuntu-user

ubuntu-root: \
	ubuntu-apt \
	ubuntu-pip

ubuntu-user: \
	ubuntu-home

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

ubuntu-pip:
	apt-get install -y python3-pip
	pip3 install -r /vagrant/requirements.txt

ubuntu-home:
	# Build home directory and configs.
	touch .hushlogin
	ln -s /vagrant vagrant
	echo "$$BASHRC" >> "${HOME_DIR}/.bashrc"
	echo "$$SCREENRC" >> "${HOME_DIR}/.screenrc"
	echo "$$MYCNF_USER" >> "${HOME_DIR}/.my.cnf"
	echo "$$CONFIG_JSON" > "${HOME_DIR}/vagrant/config.json"

