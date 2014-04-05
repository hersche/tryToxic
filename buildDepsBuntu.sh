#!/bin/bash
sudo apt-get install build-essential libtool autotools-dev automake checkinstall check git yasm python3-crypto python3-pyqt4 python3-dev
mkdir build
cd build
git clone git://github.com/jedisct1/libsodium.git
cd libsodium
./autogen.sh
./configure && make check
sudo checkinstall --install --pkgname libsodium --pkgversion 0.4.2 --nodoc
sudo ldconfig
cd ..
git clone git://github.com/irungentoo/ProjectTox-Core.git
cd ProjectTox-Core
autoreconf -i
./configure
make
sudo make install
cd ..
git clone https://github.com/aitjcize/PyTox.git 
cd PyTox
sudo python3 setup.py install