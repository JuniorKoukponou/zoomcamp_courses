#!/bin/bash

# chmod +x  install_python.sh
# sh install_python.sh
VERSION=3.11.8
wget https://www.python.org/ftp/python/$VERSION/Python-$VERSION.tgz
tar -xf Python-$VERSION.tgz

cd  Python-$VERSION/
./configure --enable-optimizations

make -j $(nproc)

sudo make altinstall

curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

