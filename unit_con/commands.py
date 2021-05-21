import socket
from actions import servo_con

def command_router(command):
    
    if command[0] == "<SERVO_MOVE>":
        servo_command(command)
        
    elif command[0] == "<CPU_COMD>":
        cpu_comd(command)
        
   

def servo_command(command):
    
    # CUSTOM/NORMAL SERVO MOVE
    if command[1] != "centre":
    
        try:
            axis = command[1]
            position = command[2]
            print(f"{self.label} {axis.upper()} servo move to {position}")
            servo_con.rotate(position, axis)
            print(f"{self.label} Command complete")
        except:
            print(f"{self.label} Invalid servo move command")
    
    # CENTRE ONE OR BOTH SERVOS
    elif command[1] == "centre" or command[1] == "center":
        if command[2] == "rotate" or command[2] == "x":
            try:
                servo_con.centre_rotate()
                print(f"{self.label} Centred X and Y servo axis")
            except Exception as e:
                print(f"{self.label} Servo error: {e}")
                
        elif command[2] == "elevate" or command[2] == "y":
            try:
                servo_con.centre_elevate()()
                print(f"{self.label} Centred X servo axis")
            except Exception as e:
                print(f"{self.label} Servo error: {e}")
                
        elif command[2] == "both" or not command[2]:
            try:
                servo_con.centre_both()
                print(f"{self.label} Centred Y servo axis")
            except Exception as e:
                print(f"{self.label} Servo error: {e}")
                
def cpu_comd(command):
    pass