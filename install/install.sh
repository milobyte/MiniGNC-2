#!/bin/bash
# script to install necessary dependencies

# installing mininet
sudo apt-get -y install mininet

# install python3-venv
sudo apt-get -y install python3-venv

# installing OpenFlow switch, controller, and Wireshark
git clone git://github.com/mininet/mininet
mininet/util/install.sh -fw

# create venv
python3 -m venv venv

# activate venv
. ./venv/bin/activate

# install dependencies
pip install -r requirements.in

