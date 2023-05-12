
-include .env

TMP_PATH=/tmp/local
OPENMPI=openmpi-4.1.5
PYTHON_VERSION=3.9
PYTHON=python$(PYTHON_VERSION)
REQUIREMENT_FILE=requirements.txt
SSH_KEY_FNAME := $(strip id_ed25519_$(subst .,_,$(shell hostname -I)))
HOST_CIDR := $(shell ip route | grep src | grep eth0 | grep /)
HOST_CIDR := $(firstword $(HOST_CIDR))


all: install-python install-native-openmpi install-sample-app refresh-env

install-python:
	sudo dnf update -y
	sudo dnf install python39 python39-devel -y
	sudo dnf install openssl-devel libffi-devel wget -y

	$(PYTHON) -m pip install pip --upgrade --user
	$(PYTHON) --version

install-native-openmpi:
	sudo dnf makecache --refresh
	sudo dnf -y install gcc-c++ perl
	sudo mkdir -p $(TMP_PATH)

ifeq ($(shell test ! -f $(OPENMPI).tar.bz2 && echo yes), yes)
	wget https://download.open-mpi.org/release/open-mpi/v4.1/$(OPENMPI).tar.bz2
endif

	sudo tar -jxf $(OPENMPI).tar.bz2 -C $(TMP_PATH)
	sudo rm openmpi-4.1.5.tar.bz2

	cd $(TMP_PATH)/$(OPENMPI) && sudo ./configure --prefix=/opt/openmpi

	sudo make -C $(TMP_PATH)/openmpi-4.1.5 all
	sudo make -C $(TMP_PATH)/openmpi-4.1.5 install

	echo "export PATH=$$PATH:/opt/openmpi/bin" >> $(HOME)/.bashrc
	echo "export LD_LIBRARY_PATH=$$LD_LIBRARY_PATH:/opt/openmpi/lib" >> $(HOME)/.bashrc

refresh-env:
	# Refresh environment variables
	exec bash

conf-nfs-server:
	sudo dnf install nfs-utils

ifeq ($(shell test ! -f $(HOME)/.ssh/id_rsa && echo yes), yes)
	ssh-keygen -t rsa -N "" -f $(HOME)/.ssh/id_rsa
	sudo chmod 400 $(HOME)/.ssh/id_rsa
endif
	cat $(HOME)/.ssh/id_rsa.pub >> $(HOME)/.ssh/authorized_keys

ifeq ($(HOST_CIDR),)
	$(error 'Please set HOST CIDR via `make configure-node HOST_CIDR=10.0.0.0/20`')
endif
	@echo Exporting NFS directories \"/home $(HOST_CIDR)\" and \"/opt $(HOST_CIDR)\".
	sudo sh -c "echo '/home $(HOST_CIDR)(rw,no_root_squash)' >> /etc/exports"
	sudo sh -c "echo '/opt $(HOST_CIDR)(rw,no_root_squash)' >> /etc/exports"

	sudo systemctl enable nfs-server
	sudo systemctl start nfs-server

conf-nfs-client:
ifeq ($(NFS_IP_ADDR),)
	$(error 'Please set NFS Server ip address via `make configure-node NFS_IP_ADDR=10.0.0.120`')
endif

	$(MAKE) install-python
	sudo dnf install nfs-utils

	@echo Mounting '/home' and '/opt' directories to NFS_SERVER:$(NFS_IP_ADDR).
	$(shell cd / && sudo mount $(NFS_IP_ADDR):/home /home && sudo mount $(NFS_IP_ADDR):/opt /opt)

ifeq ($(shell test ! -f $(HOME)/.ssh/$(SSH_KEY_FNAME) && echo yes), yes)
	ssh-keygen -t ed25519 -N "" -f $(HOME)/.ssh/$(SSH_KEY_FNAME)
	sudo chmod 400 $(HOME)/.ssh/$(SSH_KEY_FNAME)
endif
	cat $(HOME)/.ssh/$(SSH_KEY_FNAME).pub >> $(HOME)/.ssh/authorized_keys
	sudo setsebool -P use_nfs_home_dirs 1

install-sample-app:
ifeq ($(shell test ! -f .env && echo yes), yes)
	$(error Please create .env file and specify sample mpi app git url.)
endif

ifeq ($(wildcard public-materials),)
	sudo dnf install git -y
	git clone $(APP_URL) public-materials
endif
	@cd public-materials && git pull
	
	env MPICC=/opt/openmpi/bin/mpicc pip3.9 install -r public-materials/mpi/sample-app/requirements.txt