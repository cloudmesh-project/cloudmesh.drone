Crazyflie (Ubuntu 16.04):
===================
 
Crazyflie Drivers/Client Install
-----------------------------------------
(https://github.com/bitcraze/crazyflie-clients-python/blob/develop/README.md) 

- Install cflib https://github.com/bitcraze/crazyflie-lib-python (‘pip3 install cflib’ seems to work)
- Modify group settings to access USB radio without root:

	- echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="1915", ATTRS{idProduct}=="7777", MODE="0664", GROUP="plugdev"' | sudo tee /etc/udev/rules.d/99-crazyradio.rules 
	
	- echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="0483", ATTRS{idProduct}=="5740", MODE="0664", GROUP="plugdev"' | sudo tee /etc/udev/rules.d/99-crazyflie.rules
	
- Install crazyflie client https://github.com/bitcraze/crazyflie-clients-python/tree/develop

- Client can now be run system-wide with ‘cfclient’
 
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
- cd into catkin workspace src folder ‘cd ~/catkin_ws/src’
- clone git files: ‘git clone https://github.com/whoenig/crazyflie_ros.git’ *(may need to move files from crazyflie_ros folder to src folder)
- cd into workspace ‘cd ~/catkin_ws’
- 'catkin_make'

Flash firmware for crazyflie
-----------------------------------
(https://wiki.bitcraze.io/doc:crazyflie:client:pycfclient:index#bootloader):

- Connect crazyflie via usb, power on crazyflie into debug mode by holding power button for 3 seconds
- Start cfclient (do not connect crazyflie in cfclient)
- Choose configure -> bootloader
- Click “initiate bootloader cold boot”
- Choose firmware .zip (download https://github.com/bitcraze/crazyflie-release/releases) (*need zalman for LOCO positioning)
- Click “program”
- Click “restart in firmware mode”
 
Flash firmware for loco positioning node
-------------------------------------
(https://github.com/bitcraze/lps-node-firmware)

- git clone https://github.com/bitcraze/lps-node-firmware.git
- cd lps-node-firmware
- git submodule init
- git submodule update
- make
- sudo apt-get install dfu-util
- Plug node into usb while holding DFU button, should be constant blue light
- sudo make dfu