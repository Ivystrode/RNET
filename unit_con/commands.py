import os
import socket, subprocess
import time

from control import servo_con, cpu_con, cam_con, wifi_con, rad_con

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
                print("Stopping video live stream first")
                subprocess.run(['sudo','service','motion','stop'])
            cam_con.capt_img(hub_addr)
        else:
            print("not ready yet")
            
    elif command[0] == "<WIFI>":
        wifi_con.wifi_control(command, hub_addr)
        
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
            print(f"{label} {axis.upper()} servo move to {position}")
            servo_con.rotate(position, axis)
            print(f"{label} Command complete")
        except:
            print(f"{label} Invalid servo move command")
    
    # CENTRE ONE OR BOTH SERVOS
    elif command[1] == "centre" or command[1] == "center":
        if command[2] == "rotate" or command[2] == "x":
            try:
                servo_con.centre_rotate()
                print(f"{label} Centred X servo axis")
            except Exception as e:
                print(f"{label} Servo error: {e}")
                
        elif command[2] == "elevate" or command[2] == "y":
            try:
                servo_con.centre_elevate()()
                print(f"{label} Centred Y servo axis")
            except Exception as e:
                print(f"{label} Servo error: {e}")
                
        elif command[2] == "both" or not command[2]:
            try:
                servo_con.centre_both()
                print(f"{label} Centred X and Y servo axis")
            except Exception as e:
                print(f"{label} Servo error: {e}")
                
    # AUTOROTATE - SCAN CAMERA BACK AND FORTH
    elif command[1] == "<AUTOROTATE>":
        servo_con.autorotate()
                
def cpu_comd(command):
    
    if command[1] == "reboot":
        print(f"{label} Rebooting...")
        time.sleep(2)
        cpu_con.reboot()