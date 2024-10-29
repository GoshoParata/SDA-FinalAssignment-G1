import threading
import DoBotArm as dbt
import time
from serial.tools import list_ports
from DoBotArm.RobotArmClass import RobotArm
from DoBotArm import DoBotArm

# x axis is perpendicular to the convayor
# y axis is parallel to the convayor
# z axis is vertical

class Item:
    def __init__(self, position):
        self.position = position

    def getPosition(self):
        return self.position

# Define the home position coordinates
homeX, homeY, homeZ = [209, 0, 17]      # Home is above the convayor

# Create an instance of the RobotArm
robot_arm = RobotArm("COM10", homeX, homeY, homeZ, home=True)

# Create an instance of Item with raw coordinates
item = Item([(300, 300), (300, 250)])
robot_arm.statusCheck()


# the objects should be caried at z = 17
# the objects should be picked up at z = -40
# the arm should move trough position 209, -160, 17


robot_arm.moveTo([209, 0, 17])
robot_arm.moveTo([209, -160, 17])

item_position = item.getPosition()
#item1 = robot_arm.getItemPosition()
item1pos = robot_arm.processRawCoordinates(item_position)
robot_arm.moveTo(item1pos[0])
robot_arm.moveTo([209, -160, 17])