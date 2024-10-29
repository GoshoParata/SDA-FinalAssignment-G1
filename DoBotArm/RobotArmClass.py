import threading
import DoBotArm as dbt
import time
from serial.tools import list_ports
#from DoBotArm import DoBotArm
from GUI import GUI

class RobotArm:
    def __init__(self, port, homeX, homeY, homeZ, home= True):
        self.homePosition = [homeX, homeY, homeZ]  # Array containing the home position coordinates
        self.ctrlDobot = dbt.DoBotArm(port, homeX, homeY, homeZ, home= True) 
        self.ctrlDobot.moveArmXYZ(x= homeX, y= homeY, z= homeZ)
        self.status = "Idle"
        self.conveyor_running = False


    def moveTo(self, coordinates):
        x, y, z = coordinates
        # Define the limits for the arm's reach
        x_min, x_max = -255, 255
        y_min, y_max = -255, 255
        z_min, z_max = -50, 69

        # Check if the coordinates are within the limits
        if not (x_min <= x <= x_max and y_min <= y <= y_max and z_min <= z <= z_max):
            self.status = "Error"
            raise ValueError(f"Coordinates ({x}, {y}, {z}) are out of reach. "
                            f"Limits are x: [{x_min}, {x_max}], y: [{y_min}, {y_max}], z: [{z_min}, {z_max}].")

        # Move the arm to the specified coordinates
        self.status = "Moving"
        self.statusCheck()
        self.ctrlDobot.moveArmXYZ(x=x, y=y, z=z)
        #self.status = "Idle"
        #self.statusCheck()

    def getItemPosition(self, item):
        # Get the item's position from the Item class
        itemPosition = item.getPosition()
        return itemPosition

    def pickUpItem(self):
        self.ctrlDobot.toggleSuction()

    def statusCheck(self):
        print(f"Arm status: {self.status}")

    def processRawCoordinates(self, itemPosition):
        # Transformation coefficients
        a, b, c = -0.675, 0, 437.09
        d, e, f = 0, 0.7, -360
        
        # Convert each (x, y) pair in the input list
        mm_coords = []
        for x, y in itemPosition:
            x_mm = a * x + b * y + c
            y_mm = d * x + e * y + f
            mm_coords.append([x_mm, y_mm, -40])
        
        return mm_coords

    def DoConvayor(self):
        if self.conveyor_running:
            self.ctrlDobot.SetConveyor(enabled=False)
            self.conveyor_running = False
        else:
            self.ctrlDobot.SetConveyor(enabled=True, speed=15000)
            print("Conveyor is running22222")
            self.conveyor_running = True
        

    