#!/bin/bash

# install anaconda2
wget https://repo.continuum.io/archive/Anaconda2-4.3.1-Linux-x86_64.sh

# update apt-get
sudo apt-get update

# install pip
sudo apt-get install python-pip

# install pandas
sudo pip install pandas

# install numpy scipy
sudo pip install numpy scipy

# install sklearn
sudo apt-get install build-essential python-dev python-numpy \
python-setuptools python-scipy libatlas-dev libatlas3-base

sudo apt-get install python-matplotlib

pip install -U scikit-learn

# install psycopg2
apt-get install python-psycopg2

# for tmux
export TERM=xterm >> /home/ubuntu/.bashrc
source /home/ubuntu/.bashrc

# capstone psycopg2/psql
export USER='postgres'
export HOST='52.53.72.68'
export PASSWORD='postgres'
export DBNAME='stack_overflow'

export DSN='sosql2'
# export UID='SA'
export PWD='Corinn3!'
export DATABASE='ms_stack_overflow'
