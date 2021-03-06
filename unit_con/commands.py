import os
import socket, subprocess
import time, threading
from control import servo_con, cpu_con, cam_con, wifi_con, rad_con
from drone_control import drone_control, dronekit_con

label = "[" + socket.gethostname().upper() + "]"

def command_router(command, hub_addr):
    print("command router")
    
    if command[0] == "<SERVO_MOVE>":
        servo_command(command)
        
    elif command[0] == "<CPU_COMD>":
        cpu_comd(command)
        
    elif command[0] == "<SEND_FILE>":
        if command[1] == "image":
            camera_status = os.system('systemctl is-active --quiet motion')
            if camera_status == 0:
                print(f"{label} COMMANDS: Stopping video live stream")
                # subprocess.run(['sudo','service','motion','stop'])
                cam_con.stop_stream()
                time.sleep(2)
            cam_con.capt_img(hub_addr)
            print(f"{label} COMMANDS: Restarting video live stream")
            time.sleep(2)
            # subprocess.run(['sudo','service','motion','start'])
            cam_con.start_stream()
            print(f"{label} COMMANDS: Live streaming active")
        else:
            print(f"{label} DEBUG: not ready yet")
            
    elif command[0] == "<WIFI>":
        wifi_con.wifi_control(command, hub_addr)
    elif command[0] == "<FC_COMD>":
        print(F"{label} COMMANDS: FC command...")
        dronekit_con.command_subrouter(command)
        
    elif command[0] == "<VIDEO>":
        print("VIDEO COMD")
        # camera_status = os.system('systemctl is-active --quiet motion')
        # if camera_status == 0:
        #     print("Stopping video live stream first")
        # else:
            # vid_stream.run()
        cam_con.command_subrouter(command)
            
def servo_command(command):
    
    # CUSTOM/NORMAL SERVO MOVE
    if command[1] != "centre":
    
        try:
            axis = command[1]
            position = command[2]
            print(f"{label} COMMANDS: {axis.upper()} servo move to {position}")
            servo_con.rotate(position, axis)
            print(f"{label} COMMANDS: Command complete")
        except:
            print(f"{label} COMMANDS: Invalid servo move command")
    
    # CENTRE ONE OR BOTH SERVOS
    elif command[1] == "centre" or command[1] == "center":
        if command[2] == "rotate" or command[2] == "x":
            try:
                servo_con.centre_rotate()
                print(f"{label} COMMANDS: Centred X servo axis")
            except Exception as e:
                print(f"{label} COMMANDS: Servo error: {e}")
                
        elif command[2] == "elevate" or command[2] == "y":
            try:
                servo_con.centre_elevate()()
                print(f"{label} COMMANDS: Centred Y servo axis")
            except Exception as e:
                print(f"{label} COMMANDS: Servo error: {e}")
                
        elif command[2] == "both" or not command[2]:
            try:
                servo_con.centre_both()
                print(f"{label} COMMANDS: Centred X and Y servo axis")
            except Exception as e:
                print(f"{label} COMMANDS: Servo error: {e}")
                
    # AUTOROTATE - SCAN CAMERA BACK AND FORTH
    elif command[1] == "<AUTOROTATE>":
        servo_con.autorotate()
                
def cpu_comd(command):
    
    if command[1] == "reboot":
        print(f"{label} COMMANDS: Rebooting...")
        time.sleep(2)
        cpu_con.reboot()