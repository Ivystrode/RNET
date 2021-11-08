from pymavlink import mavutil
import time
"""
Drone control. The functions have some really long lines, blame mavlink, that's just how it is.
THIS WOULD BE A LOT NICER WITH DRONEKIT
THIS WOULD BE A LOT NICER WITH DRONEKIT
THIS WOULD BE A LOT NICER WITH DRONEKIT
THIS WOULD BE A LOT NICER WITH DRONEKIT
"""

# REMEMBER!!! MAKE SURE ARM PARAMETERS ARE SET TO 0 OR 1 AS REQUIRED

# Note - link/assign unit model to UDP port --- ? Can be a model attribute
# how about we make a drone Class that can be instantiated by models individually...maybe

# ==========INITIATE==========
fc_connection = mavutil.mavlink_connection('udpin:localhost:14551') # creates a UDP socket to *listen* on said port - udpout *initiates* an IP connection
# 14550 used for GCS to monitor vehicle

# we are going to need to use multiple ports for multiple vehicles - both inbound and outbound

# Check for connection...
fc_connection.wait_heartbeat() 
print(f"=====Receiving Telemetry! {fc_connection.target_system} -- {fc_connection.target_component}=====")

# Get initial location
msg = fc_connection.recv_match(type="TERRAIN_REPORT", blocking=True)
coords = [msg.lat, msg.lon]
print(f"Vehicle location: {coords} | Alt: {msg.current_height}")

# ==========ARM==========
# ARM - connection.target_system & component is filled in when we receive the heartbeat from the vehicle
def arm_disarm(which: int):
    if which > 1:
        print("Function takes either 0 or 1 disarm/arm")
    else:
        fc_connection.mav.command_long_send(fc_connection.target_system,
                                            fc_connection.target_component,
                                            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
                                            0, # generic parameter - then 7 parameters of COMMAND_LONG
                                            which, # param 1 of the ARM_DISARM command - see mavlink docs for info. 0 means disarm, 1 means arm
                                            0, # this correlates to the FORCE parameter of ARM_DISARD
                                            0,0,0,0,0 # now we fill in the rest of the empty params as 0s
                                            )

        msg = fc_connection.recv_match(type="COMMAND_ACK", blocking=True)
        print(msg)
    # see result param of the ACK message - it corresponds to MAV_RESULT result code. 0 means accepted/it worked

# ==========TAKEOFF==========
# note when passing lat and long params as 0 location sets to vehicle current location
def takeoff(alt):
    fc_connection.mav.command_long_send(fc_connection.target_system,
                                        fc_connection.target_component,
                                        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
                                        0, # generic parameter - then 7 parameters of COMMAND_LONG
                                        0, # pitch - plane only
                                        0, # empty
                                        0, # empty
                                        0, # yaw - if magnetometer present only
                                        0, # latitude
                                        0, # longitude
                                        alt  # altitude (m)
                                        )

    # # listen for ACK from the command so we know if it worked or not
    msg = fc_connection.recv_match(type="COMMAND_ACK", blocking=True)
    print(msg)
    
def travel(x: int, y: int, z: int, vX: int):
    """
    Basic move command relative to current position
    """
    fc_connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10,
                                                                                         fc_connection.target_system,
                                                                                         fc_connection.target_component,
                                                                                         mavutil.mavlink.MAV_FRAME_LOCAL_NED,
                                                                                         int(0b100111110000), # type mask...image its a series of o(off) and 1(on) for the below features of this function. In reverse order. So you need to switch some on and some off
                                                                                         x, # forward
                                                                                         y,# right/left
                                                                                         z, # negative is UPWARDS!!!
                                                                                         vX, #vX
                                                                                         0, #vY
                                                                                         0, #vZ
                                                                                         0,
                                                                                         0,
                                                                                         0,
                                                                                         1.57, # yaw "target" - somehow 1.57 is 90 degrees to the right?!
                                                                                         0.5)) # yaw_rate
    # 51.80409 -4.06425
def global_travel():
    """
    Move to geographic coordinates
    """
    fc_connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_global_int_message(10,
                                                                                         fc_connection.target_system,
                                                                                         fc_connection.target_component,
                                                                                         mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                                                                                         int(0b110111111000), 
                                                                                         int(51.0912324 * 10 ** 7), # have to do them to the power of 10...
                                                                                         int(-4.0896606 * 10 ** 7),
                                                                                         55, # needs to be POSITIVE to go up in this one
                                                                                         0, #vX
                                                                                         0, #vY
                                                                                         0, #vZ
                                                                                         0,
                                                                                         0,
                                                                                         0,
                                                                                         0, # yaw "target" - somehow 1.57 is 90 degrees to the right?!
                                                                                         0)) # yaw_rate
    while True:
        msg = fc_connection.recv_match(type="LOCAL_POSITION_NED", blocking=True)
        print(msg)
if __name__ == '__main__':
    arm_disarm(1)
    takeoff(24)
    time.sleep(5)
    global_travel()