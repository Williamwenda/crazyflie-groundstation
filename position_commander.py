# -*- coding: utf-8 -*-
#
#     ||          ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
#  Copyright (C) 2018 Bitcraze AB
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA  02110-1301, USA.
"""
This script shows the basic use of the PositionHlCommander class.

Simple example that connects to the crazyflie at `URI` and runs a
sequence. This script requires some kind of location system.

The PositionHlCommander uses position setpoints.

Change the URI variable to your Crazyflie configuration.
"""
import time
import logging
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncLogger import SyncLogger

from cflib.positioning.position_hl_commander import PositionHlCommander

# URI to the Crazyflie to connect to
uri = 'radio://0/120/2M/E7E7E7EC1D' 
# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

def slightly_more_complex_usage():
    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
        with PositionHlCommander(
                scf,
                x=0.0, y=0.0, z=0.0,
                default_velocity=0.3,
                default_height=0.5,
                controller=PositionHlCommander.CONTROLLER_PID) as pc:
            # Go to a coordinate
            pc.go_to(1.0, 1.0, 1.0)

            # Move relative to the current position
            pc.right(1.0)

            # Go to a coordinate and use default height
            pc.go_to(0.0, 0.0)

            # Go slowly to a coordinate
            pc.go_to(1.0, 1.0, velocity=0.2)

            # Set new default velocity and height
            pc.set_default_velocity(0.3)
            pc.set_default_height(1.0)
            pc.go_to(0.0, 0.0)


def simple_sequence():
    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
        with PositionHlCommander(scf) as pc:
            # pc.forward(1.0)
            # pc.left(1.0)
            # pc.back(1.0)
            pc.go_to(0.0, 0.0, 1.0)
            time.sleep(10)

def simple_connect():
    print("I'm connected! :D")
    time.sleep(10)
    print("Now I will disconnect...")

def simple_log(scf, logconf):
    with SyncLogger(scf, logconf) as logger:
        for log_entry in logger:
            timestamp = log_entry[0]
            data = log_entry[1]
            logconf_name = log_entry[2]
            # the logged data is a dict
            values = data.values()
            keys = data
            print('[%d][%s]: %s' % (timestamp, logconf.name, data))
            
            # break
def log_stab_callback(timestamp, data, logconf):
    print('[%d][%s]: %s' % (timestamp, logconf.name, data))
    
def simple_log_async(scf, logconf):
    cf = scf.cf
    cf.log.add_config(logconf)
    logconf.data_received_cb.add_callback(log_stab_callback)
    logconf.start()
    time.sleep(5)
    logconf.stop()


if __name__ == '__main__':
    cflib.crtp.init_drivers(enable_debug_driver=False)
    
    lg_stab = LogConfig(name='Stabilizer', period_in_ms=10)
    lg_stab.add_variable('stabilizer.roll', 'float')
    lg_stab.add_variable('stabilizer.pitch', 'float')
    lg_stab.add_variable('stabilizer.yaw', 'float')
    
    # log uwb tdoa2 measurements 
    lg_uwb1 = LogConfig(name='tdoa2', period_in_ms=10)
    lg_uwb1.add_variable('tdoa2.d7-0', 'float')
    lg_uwb1.add_variable('tdoa2.d0-1', 'float')
    lg_uwb1.add_variable('tdoa2.d1-2', 'float')
    lg_uwb1.add_variable('tdoa2.d2-3', 'float')
    
        # log uwb tdoa2 measurements 
    lg_uwb2 = LogConfig(name='tdoa2', period_in_ms=10)
    lg_uwb2.add_variable('tdoa2.d3-4', 'float')
    lg_uwb2.add_variable('tdoa2.d4-5', 'float')
    lg_uwb2.add_variable('tdoa2.d5-6', 'float')
    lg_uwb2.add_variable('tdoa2.d6-7', 'float')

    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
        
        # simple_log_async(scf, lg_stab)
        
        simple_log(scf, lg_uwb1)
        
        # simple_connect()
        # simple_sequence()
        # slightly_more_complex_usage()

