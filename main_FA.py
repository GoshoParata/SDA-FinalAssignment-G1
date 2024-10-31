import threading
import time
from RobotArmClass import RobotArm
from GUI import GUI

# Initialize the RobotArm and GUI
robot_arm = RobotArm("COM9", home=True)
print("Robot arm initialized.")

gui = GUI(False, [], False, "")
print("GUI initialized.")

# Flag to indicate when the "Run DoBot" button is pressed
run_dobot_flag = threading.Event()

# Override the runDobot method in GUI to trigger robot arm movement
def run_dobot_override():
    selected_coordinates = gui.getSelectedCoordinates()
    print(f"Running DoBot with coordinates: {selected_coordinates}")
    if selected_coordinates:
        # Transform the pixel coordinates to robot coordinates
        transformed_coordinates = robot_arm.processRawCoordinates(selected_coordinates)
        print(f"Transformed coordinates: {transformed_coordinates}")
        # Move the robot arm to pick up items
        robot_arm.moveTo(transformed_coordinates)
    run_dobot_flag.set()

# Override the default runDobot method in GUI
gui.runDobot = run_dobot_override

# Function to run the GUI
def run_gui():
    print("Starting GUI...")
    gui.initCamera()
    print("GUI started.")

# Function to monitor DoBot operations
def monitor_dobot():
    print("Waiting for user to select items and press 'Run DoBot'...")
    while True:
        run_dobot_flag.wait()  # Wait until the flag is set
        run_dobot_flag.clear()  # Clear the flag for the next run
        time.sleep(1)  # Small delay before next check

# Start the GUI and monitoring in separate threads
gui_thread = threading.Thread(target=run_gui)
dobot_thread = threading.Thread(target=monitor_dobot)

print("Starting threads...")
gui_thread.start()
dobot_thread.start()

# Wait for both threads to complete
gui_thread.join()
dobot_thread.join()
print("Application completed.")