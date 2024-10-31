import threading
import DoBotArm as dbt
import time
from serial.tools import list_ports
from DoBotArm import DoBotArm

class RobotArm:
    def __init__(self, port, home= True):
        self.homePosition = [209, 0, 17]  # Array containing the home position coordinates
        self.ctrlDobot = dbt.DoBotArm(port, self.homePosition[0], self.homePosition[1], self.homePosition[2], home= True) 
        self.ctrlDobot.moveArmXYZ(x=self.homePosition[0], y=self.homePosition[1], z=self.homePosition[2])
        self.conveyor_running = False


    def moveTo(self, coordinates_list):
        # Define the limits for the arm's reach

        # x axis is perpendicular to the conveyor
        # y axis is parallel to the conveyor
        # z axis is vertical

        x_min, x_max = -255, 255
        y_min, y_max = -255, 255
        z_min, z_max = -50, 69

        self.DoConveyor()   # Start the conveyor
        for coordinates in coordinates_list:
            x, y, z = coordinates

            # Check if the coordinates are within the limits
            if not (x_min <= x <= x_max and y_min <= y <= y_max and z_min <= z <= z_max):
                raise ValueError(f"Coordinates ({x}, {y}, {z}) are out of reach. "
                                 f"Limits are x: [{x_min}, {x_max}], y: [{y_min}, {y_max}], z: [{z_min}, {z_max}].")

            # The moving starts from the home position
            self.ctrlDobot.moveArmXYZ(x=self.homePosition[0], y=self.homePosition[1], z=self.homePosition[2])
            # The arm must move through [209, -160, 17] to avoid collisions
            self.ctrlDobot.moveArmXYZ(x=209, y=-160, z=17)
            # Move the arm to the specified coordinates
            self.ctrlDobot.moveArmXYZ(x=x, y=y, z=z)
            # Pick up the item
            self.pickUpItem()
            # The arm must move through [209, -160, 17] to avoid collisions
            self.ctrlDobot.moveArmXYZ(x=209, y=-160, z=17)
            # The moving finishes the movement at the home position
            self.ctrlDobot.moveArmXYZ(x=self.homePosition[0], y=self.homePosition[1], z=self.homePosition[2])
            # Drop of the item
            self.pickUpItem()
            time.sleep(2)

        self.DoConveyor()   # Stop the conveyor

    def pickUpItem(self):
        self.ctrlDobot.toggleSuction()

    def processRawCoordinates(self, itemPosition):
        # Transformation coefficients
        a, b, c = -0.675, 0, 427.09
        d, e, f = 0, 0.7, -360
        
        # Convert each (x, y) pair in the input list
        mm_coords = []
        for x, y in itemPosition:
            x_mm = a * x + b * y + c
            y_mm = d * x + e * y + f
            mm_coords.append([x_mm, y_mm, -40])
        
        return mm_coords

    def DoConveyor(self):
        if self.conveyor_running:
            self.ctrlDobot.SetConveyor(enabled=False)
            self.conveyor_running = False
        else:
            self.ctrlDobot.SetConveyor(enabled=True, speed=15000)
            print("Conveyor is running22222")
            self.conveyor_running = True
        

    