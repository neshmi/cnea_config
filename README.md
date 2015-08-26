# CNEA Cave Configuration

## IP Configurations
192.168.10.1    headnode
192.168.10.2    cnea-0
192.168.10.3    cnea-1
192.168.10.4    cnea-2
192.168.10.5    cnea-3
192.168.10.6    cnea-4

## interfaces file
auto eth0
iface eth0 inet static
address 192.168.10.???
netmask 255.255.255.0
network 192.168.10.0
broadcast 192.168.10.255
gateway 192.168.10.1
dns-nameservers 8.8.8.8 8.8.4.4
 
## All Packages

sudo apt-get install openssh-server vim build-essential git libmxml-dev cmake-curses-gui libopenscenegraph-dev openscenegraph osgearth libosgearth-dev libglew-dev libsdl-dev libtiff4-dev

### Basic, non CalVR related
openssh-server vim build-esential git

### General requirements  
libmxml-dev cmake-curses-gui

### OSG (Current version has a font bug, maybe build older OSG from source?)
libopenscenegraph-dev openscenegraph osgearth libosgearth-dev

### PanoLOD Requirements
libglew-dev libsdl-dev
libtiff4 (FROM SOURCE)

## LGRemote (https://github.com/dreamcat4/lgremote)

*Work in Progress* 

We need to get the information together to be able to remotely start and stop all TVs, putting them in 3D remotely as well.

RE: ChrisM, latest LG TVs have changed protocol, this may not work. Follow project, however.
