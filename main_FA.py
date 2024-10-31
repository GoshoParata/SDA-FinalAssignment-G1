import threading
import time
from RobotArmClass import RobotArm
from GUI import GUI



# Define the home position coordinates
homeX, homeY, homeZ = [209, 0, 17]  # Home is above the conveyor

# Create an instance of the RobotArm
robot_arm = RobotArm("COM10", home=True)
print("Robot arm initialized.")

# Initialize the GUI
gui = GUI(False, [], False, "")
print("GUI initialized.")

# Flag to indicate when the "Run DoBot" button is pressed
run_dobot_flag = threading.Event()

# Modify the runDobot method in the GUI class to set the flag
def run_dobot_override():
    selected_coordinates = gui.getSelectedCoordinates()
    print(f"Running DoBot with coordinates: {selected_coordinates}")
    run_dobot_flag.set()

gui.runDobot = run_dobot_override

# Function to run the GUI
def run_gui():
    print("Starting GUI...")
    gui.initCamera()
    print("GUI started.")

# Function to run the DoBot arm operations
def run_dobot():
    print("Waiting for user to select items and press 'Run DoBot'...")
    processed_coordinates = set()
    while True:
        run_dobot_flag.wait()  # Wait until the flag is set
        run_dobot_flag.clear()  # Clear the flag for the next run

        selected_coordinates = gui.getSelectedCoordinates()
        new_coordinates = [coord for coord in selected_coordinates if tuple(coord) not in processed_coordinates]
        if new_coordinates:
            print(f"New coordinates: {new_coordinates}")

            # Use the new coordinates in the robot arm operations
            transformed_coordinates = robot_arm.processRawCoordinates(new_coordinates)
            robot_arm.moveTo(transformed_coordinates)
            print("DoBot arm operations completed.")

            # Add the new coordinates to the processed set
            processed_coordinates.update(tuple(coord) for coord in new_coordinates)
        time.sleep(1)  # Check for new coordinates every second

# Run the GUI and DoBot arm operations in separate threads
gui_thread = threading.Thread(target=run_gui)
dobot_thread = threading.Thread(target=run_dobot)

print("Starting threads...")
gui_thread.start()
dobot_thread.start()

# Wait for both threads to complete
gui_thread.join()
dobot_thread.join()
print("Both threads completed.")