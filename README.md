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

install:

    cd ~/catkin_ws
    catkin_make
    catkin_make install
    source devel/setup.bash

Flash firmware for crazyflie
-----------------------------------
(https://wiki.bitcraze.io/doc:crazyflie:client:pycfclient:index):

- Connect crazyflie via usb, power on crazyflie into debug mode by holding power button for 3 seconds
- Start cfclient (do not connect crazyflie in cfclient)
- Choose connect -> bootloader
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
	
Using ROS with Crazyflie:
-------------------------
In order to use ROS, you will need to first have a catkin workspace setup. Our ROS script will create a Publisher, which published to /crazyflie/cmd_vel (command velocity) to issue commands to the Crazyflie. In turn, our script will subscrive to various nodes that the crazyflie drivers create, such as /crazyflie/imu for sensor information and /crazyflie/pose for positioning information with the loco script.

All scripts require the catkin source:

    cd ~/catkin_ws
    source devel/setup.bash

The first task it to start the ROS core:

    roscore
    
Next, use the appropriate launch script, and provide the uri "roslaunch (package) (launch script) *(options)":

    roslaunch drone single.launch uri:=radio://0/80/250K
    
You should see all of the current topics being published:

    rostopic list
    
You can echo a topic to receive information from it

    rostopic echo /crazyflie/imu
    
To run a script do "rosrun (package) (script)":

    rosrun drone test.py
    
Crazyflie and ROS
-----------------

One ROS, the crazyflie receives commands from on the /crazyflie/cmd_vel topic. The format for commands is "Twist". The Twist command receives two vectors, the first with linear acceleration and the second with angular velocity.

In Python:

    from geometry_msgs.msg import Twist, Vector3
    Twist(Vector3(pitch, roll, thrust), Vector3(_, _, yaw))
    
Crazyflie Issues
----------------

The Crazyflie firmware behaves as if the drone is being controlled with a joystick. Therefore, the first value sent should be all zeroes, or the drone will not respond to any commands. If there is any break in the input (such as the drone landing, then taking off later), the zero values will have to be sent again.

Python:

    cf.commander.send_setpoint(0, 0, 0, 0)
    
ROS (use empty Twist):

    publisher.publish(Twist())
