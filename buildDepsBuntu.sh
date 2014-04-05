#!/bin/bash
sudo apt-get install build-essential libtool autotools-dev automake checkinstall check git yasm python3-crypto python3-pyqt4 python3-dev
mkdir build
cd build
#libsodium
git clone git://github.com/jedisct1/libsodium.git
cd libsodium
./autogen.sh
./configure && make check
sudo checkinstall --install --pkgname libsodium --pkgversion 0.4.2 --nodoc
sudo ldconfig
cd ..
#opus
wget http://downloads.xiph.org/releases/opus/opus-1.0.3.tar.gz
tar xzf opus-1.0.3.tar.gz
cd opus-1.0.3
./configure
make -j3
sudo make install
cd ..
#libvpx
git clone http://git.chromium.org/webm/libvpx.git
cd libvpx
./configure --enable-shared
make -j3
sudo make install
sudo ldconfig
cd ..

#tox-core
git clone git://github.com/irungentoo/ProjectTox-Core.git
cd ProjectTox-Core
autoreconf -i
./configure
make
sudo make install
cd ..
#pytox
git clone https://github.com/aitjcize/PyTox.git 
cd PyTox
sudo python3 setup.py install