"""
Attribution:
    https://github.com/bitcraze/crazyflie-lib-python/blob/master/examples/ramp.py
"""

import time
from threading import Thread

import cflib
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig

class Drone:
    channel = 80
    bandwidth = 250
    
    # commands per second, 100 is recommended (1 every 10ms)
    precision = 100
    
    # + right, - left
    roll = -1
    # + forward, - backward
    pitch = 1.2
    yawrate = 0
    # 10001 - 65000
    thrust = 0
    
    def __init__(self):        
        cflib.crtp.init_drivers(enable_debug_driver = False)
        uri = 'radio://0/{}/{}K'.format(self.channel, self.bandwidth)
        self.connect(uri)
        
    def _connected(self, link_uri):
        """ This callback is called form the Crazyflie API when a Crazyflie
        has been connected and the TOCs have been downloaded."""
        
        self.send_setpoint(0, 0, 0, 0)
        
        # position printing
        '''log_conf = LogConfig(name='Position', period_in_ms=500)
        log_conf.add_variable('kalman.stateX', 'float')
        log_conf.add_variable('kalman.stateY', 'float')
        log_conf.add_variable('kalman.stateZ', 'float')
        self.cf.log.add_config(log_conf)
        log_conf.data_received_cb.add_callback(self.position_callback)
        log_conf.start()'''

        # Start a separate thread to do the motor test.
        # Do not hijack the calling thread!        
        Thread(target=self.fly).start()

    def _connection_failed(self, link_uri, msg):
        """Callback when connection initial connection fails (i.e no Crazyflie
        at the specified address)"""
        print('Connection to %s failed: %s' % (link_uri, msg))

    def _connection_lost(self, link_uri, msg):
        """Callback when disconnected after a connection has been made (i.e
        Crazyflie moves out of range)"""
        print('Connection to %s lost: %s' % (link_uri, msg))

    def _disconnected(self, link_uri):
        """Callback when the Crazyflie is disconnected (called in all cases)"""
        print('Disconnected from %s' % link_uri)
        
    def connect(self, uri):
        '''Creat crazyflie instance with callbacks
        '''
        self.cf = Crazyflie()
        
        self.cf.connected.add_callback(self._connected)
        self.cf.disconnected.add_callback(self._disconnected)
        self.cf.connection_failed.add_callback(self._connection_failed)
        self.cf.connection_lost.add_callback(self._connection_lost)
        
        self.cf.open_link(uri)
        
    def position_callback(timestamp, data, logconf):
        '''Callback for position printing
        '''
        x = data['kalman.stateX']
        y = data['kalman.stateY']
        z = data['kalman.stateZ']
        print('pos: ({}, {}, {})'.format(x, y, z))
        
    def fly(self):
        '''Sandbox for testing fly commands
        '''
        self.send_setpoint(thrust = 10001)
        self.increase_thrust_to(32000)
        self.decrease_thrust_to(10001, 50)
        
        self.cf.close_link()
        
    def increase_thrust_to(self, target, step = 5000):
        '''Increase thrust to target by steps
        '''
        while self.thrust < target:
            self.thrust += step
            self.send_setpoint()
            time.sleep(1 / self.precision)
        
    def decrease_thrust_to(self, target, step = 500):
        '''Decrease thrust to target by steps
        '''
        while self.thrust > target:
            self.thrust -= step
            self.send_setpoint()
            time.sleep(1 / self.precision)
        
    def hold_for(self, secs):
        '''Maintain current thrust for secs
        '''
        for _ in range(secs * 100):
            self.send_setpoint()    
            time.sleep(1 / self.precision)
            
    def set_for(self, secs, roll = None, pitch = None, yawrate = None, thrust = None, strength = 1):
        '''Set movement variables for given number of seconds
        '''
        roll = roll or self.roll
        pitch = pitch or self.pitch
        yawrate = yawrate or self.yawrate
        thrust = thrust or self.thrust
        
        for _ in range(secs * 100):
            self.send_setpoint(roll, pitch, yawrate, thrust)
            time.sleep(1 / self.precision)
            
    def send_setpoint(self, roll = None, pitch = None, yawrate = None, thrust = None):
        '''Wrapper for crazyflie send setpoint
        '''
        roll = roll or self.roll
        pitch = pitch or self.pitch
        yawrate = yawrate or self.yawrate
        thrust = thrust or self.thrust
        self.cf.commander.send_setpoint(roll, pitch, yawrate, thrust) 
             
if __name__ == '__main__':
    Drone()
