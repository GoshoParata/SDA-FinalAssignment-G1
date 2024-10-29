import math
import random
import threading
import DoBotArm as dbt
import time
from serial.tools import list_ports_common

homeX, homeY, homeZ = 170, 0, 0
ctrlDobot = dbt.DoBotArm("COM9", homeX, homeY, homeZ, home= True)
print("starting")
ctrlDobot.moveHome()

class RobotArm:
    def __init__(self):
        # Define home as past position
        self.pastPosition = [homeX, homeY, homeZ]
        
        # Define quadrant waypoints
        # z is a constant 25 to fit the largest range of movement
        self.waypoints = {
            'Q1': (150, 150, 25),
            'Q2': (-150, 150, 25),
            'Q3': (-150, -150, 25),
            'Q4': (150, -150, 25)
        }

    def get_quadrant(self, x, y):
        # Determine which quadrant a point is located in.
        if x >= 0 and y >= 0:
            return 'Q1'
        elif x < 0 and y >= 0:
            return 'Q2'
        elif x < 0 and y < 0:
            return 'Q3'
        else:
            return 'Q4'
    #basic deadzone avoidance
    def waypointMove(self, final_x, final_y, final_z):
        # Get current start position (past position)
        start_x, start_y, start_z = self.pastPosition

        # Determine start and end quadrants
        start_quadrant = self.get_quadrant(start_x, start_y)
        end_quadrant = self.get_quadrant(final_x, final_y)

        # Check if the start and end positions are in different quadrants
        if start_quadrant != end_quadrant:
            # Move through two waypoints: 
            # 1st in start quadrant
            # 2nd in end quadrant
            print("Moving through two waypoints (Start/End !same quadrant)")
            
            # First waypoint: In the starting quadrant
            waypoint1_x, waypoint1_y, waypoint1_z = self.waypoints[start_quadrant]
            ctrlDobot.moveArmXYZ(waypoint1_x, waypoint1_y, waypoint1_z)
            print(f"Moved arm to waypoint1 ({waypoint1_x}, {waypoint1_y}, {waypoint1_z})")

            # Second waypoint: In the ending quadrant
            waypoint2_x, waypoint2_y, waypoint2_z = self.waypoints[end_quadrant]
            ctrlDobot.moveArmXYZ(waypoint2_x, waypoint2_y, waypoint2_z)
            print(f"Moved arm to waypoint2 ({waypoint2_x}, {waypoint2_y}, {waypoint2_z})")

        else:
            # Move through a single waypoint if start and end are in the same quadrant
            print("Moving arm through single waypoint (Start/End same quadrant)")
            waypoint_x, waypoint_y, waypoint_z = self.waypoints[end_quadrant]
            ctrlDobot.moveArmXYZ(waypoint_x, waypoint_y, waypoint_z)
            print(f"Moved arm to waypoint0 ({waypoint_x}, {waypoint_y}, {waypoint_z})")

        # Move to the final position
        print("Moving to final position")
        ctrlDobot.moveArmXYZ(final_x, final_y, final_z)
        print(f"Moved arm to final ({final_x}, {final_y}, {final_z})")

        # Final action is to update pastPosition 
        self.pastPosition = [x, y, z]


# Example Usage:
robot = RobotArm()
#test positions
robot.waypointMove(200, -100, 50)
robot.waypointMove(200, 100, 40)
robot.waypointMove(100, 200, 40)
robot.waypointMove(0, -200, 40)
