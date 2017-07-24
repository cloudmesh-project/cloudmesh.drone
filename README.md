Crazyflie (Ubuntu 16.04):
===================
 
Crazyflie Drivers/Client Install
-----------------------------------------
(https://github.com/bitcraze/crazyflie-clients-python) 

Install cflib:

	pip3 install cflib
	
You can also use local files from https://github.com/bitcraze/crazyflie-lib-python for development
	
Modify group settings to access USB radio without root:

	echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="1915", ATTRS{idProduct}=="7777", MODE="0664", GROUP="plugdev"' | sudo tee /etc/udev/rules.d/99-crazyradio.rules 
	echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="0483", ATTRS{idProduct}=="5740", MODE="0664", GROUP="plugdev"' | sudo tee /etc/udev/rules.d/99-crazyflie.rules
	
Clone git repo:

	git clone https://github.com/bitcraze/crazyflie-clients-python.git
	cd crazyflie-clients-python
	
Install dependencies:

	sudo apt-get install python3 python3-pip python3-pyqt5

Install client:

	pip3 install -e .
	
Client can now be run system-wide with 'cfclient'
 
Using cflclient:
--------------------
- Click ‘Scan’ to find radio/usb crazyflies
- Choose Crazyflie by radio or usb
- Click ‘connect’
 
Change configuration (channel and bitrate):
-------------------------------
- Open cfclient
- Click connect -> configure 2.0
 
Install ROS
----------------
- Install ROS http://www.ros.org/install(~2.5GB)
- Install catkin http://wiki.ros.org/catkin#Installing_catkin 
- Create catkin workspace http://wiki.ros.org/catkin/Tutorials/create_a_workspace 

*note: make sure to be consistent with the version of ROS you chose to install (lunar, kinetic, etc)
 
Install Crazyflie ROS packages
------------------------------------------
- cd into catkin workspace src folder 'cd ~/catkin_ws/src'
- clone git files: 'git clone https://github.com/whoenig/crazyflie_ros.git' *(may need to move files from crazyflie_ros folder to src folder)

    cd ~/catkin_ws
    catkin_make
    catkin_make install
    source ./devel/setup.bash

Flash firmware for crazyflie
-----------------------------------
(https://wiki.bitcraze.io/doc:crazyflie:client:pycfclient:index):

- Connect crazyflie via usb, power on crazyflie into debug mode by holding power button for 3 seconds
- Start cfclient (do not connect crazyflie in cfclient)
- Choose configure -> bootloader
- Click "initiate bootloader cold boot"
- Choose firmware .zip (download https://github.com/bitcraze/crazyflie-release/releases) (*need zalman for LOCO positioning)
- Click "program"
- Click "restart in firmware mode"
 
Flash firmware for loco positioning node
-------------------------------------
(https://github.com/bitcraze/lps-node-firmware)

Clone git repo:

	git clone https://github.com/bitcraze/lps-node-firmware.git
	cd lps-node-firmware
	
Initiate/update submodules:

	git submodule init
	git submodule update
	
Make sure dfu-util is installed:

	sudo apt-get install dfu-util
	
Run make:

	make
	
Plug node into usb while holding DFU button, should be constant blue light

Run make command for dfu (sudo may be necessary):

	sudo make dfu
