import numpy as np

# File path
file_path = "C:\\Users\\Admin\\Desktop\\encode trial\\newputty.log"

# Initialize variables to store parsed data
counter = None
linear_acc = {'x': None, 'y': None, 'z': None}
quaternion = {'i': None, 'j': None, 'k': None, 'real': None}
current_time = None 

# Process the file and print parsed data for debugging
with open(file_path, 'r') as file:
    capture_data = None
    for line in file:
        line = line.strip()
        
        # Determine type of data block (L for Linear Acceleration, Q for Quaternion)
        if line.endswith("L"):
            # Start of linear acceleration data
            capture_data = "L"
            counter = int(line[:-1])
            continue
        elif line.endswith("Q"):
            # Start of quaternion data
            capture_data = "Q"
            counter = int(line[:-1])
            continue

        # Parse timestamp specifically for acceleration data
        if capture_data == "L" and line.startswith("T:"):
            current_time = int(line.split(":")[1].strip().split()[0])  # Parse timestamp in microseconds
            continue
        
        # Capture data based on type
        if capture_data == "L":
            if line.startswith("x ="):
                linear_acc['x'] = float(line.split("=")[1].strip())
            elif line.startswith("y ="):
                linear_acc['y'] = float(line.split("=")[1].strip())
            elif line.startswith("z ="):
                linear_acc['z'] = float(line.split("=")[1].strip())
            
            # Check if all linear acceleration components are captured
            if None not in linear_acc.values() and current_time is not None:
                # Process only if we have corresponding quaternion data
                if None not in quaternion.values():
                    print(f"Counter: {counter}, Time: {current_time / 1000} ms, "
                          f"Acceleration: (x = {linear_acc['x']:.6f}, y = {linear_acc['y']:.6f}, z = {linear_acc['z']:.6f}), "
                          f"Quaternion: (i = {quaternion['i']:.6f}, j = {quaternion['j']:.6f}, "
                          f"k = {quaternion['k']:.6f}, real = {quaternion['real']:.6f})")
                
                # Reset values for next capture
                linear_acc = {'x': None, 'y': None, 'z': None}
                current_time = None

        elif capture_data == "Q":
            if line.startswith("i ="):
                quaternion['i'] = float(line.split("=")[1].strip())
            elif line.startswith("j ="):
                quaternion['j'] = float(line.split("=")[1].strip())
            elif line.startswith("k ="):
                quaternion['k'] = float(line.split("=")[1].strip())
            elif line.startswith("r ="):
                quaternion['real'] = float(line.split("=")[1].strip())

            # Check if quaternion is fully captured and print with the latest linear acceleration
            if None not in quaternion.values() and None not in linear_acc.values() and current_time is not None:
                print(f"Counter: {counter}, Time: {current_time / 1000} ms, "
                      f"Acceleration: (x = {linear_acc['x']:.6f}, y = {linear_acc['y']:.6f}, z = {linear_acc['z']:.6f}), "
                      f"Quaternion: (i = {quaternion['i']:.6f}, j = {quaternion['j']:.6f}, "
                      f"k = {quaternion['k']:.6f}, real = {quaternion['real']:.6f})")
                









