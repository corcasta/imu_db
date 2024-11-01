import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Initialize lists to store positions
xvals, yvals, zvals = [0], [0], [0]

# Placeholder for time-based trapezoidal integration values
prev_time, prev_ax, prev_ay, prev_az = 0, 0, 0, 0
prev_vx, prev_vy, prev_vz = 0, 0, 0
prev_px, prev_py, prev_pz = 0, 0, 0

# Trapezoidal integration function
def trapezoidal_integration(prev_time, current_time, prev_ax, prev_ay, prev_az, 
                            current_ax, current_ay, current_az,
                            prev_vx, prev_vy, prev_vz,
                            prev_px, prev_py, prev_pz):
    dt = (current_time - prev_time) / 1_000_000  # convert microseconds to seconds

    # Velocity
    new_vx = prev_vx + 0.5 * (prev_ax + current_ax) * dt
    new_vy = prev_vy + 0.5 * (prev_ay + current_ay) * dt
    new_vz = prev_vz + 0.5 * (prev_az + current_az) * dt

    # Position
    new_px = prev_px + 0.5 * (prev_vx + new_vx) * dt
    new_py = prev_py + 0.5 * (prev_vy + new_vy) * dt
    new_pz = prev_pz + 0.5 * (prev_vz + new_vz) * dt
    
    return new_vx, new_vy, new_vz, new_px, new_py, new_pz

def quaternion_to_rotation_matrix(q):
    """Convert a quaternion into a 3x3 rotation matrix."""
    w, x, y, z = q['real'], q['i'], q['j'], q['k']
    return np.array([
        [1 - 2*y**2 - 2*z**2, 2*x*y - 2*z*w,     2*x*z + 2*y*w],
        [2*x*y + 2*z*w,       1 - 2*x**2 - 2*z**2, 2*y*z - 2*x*w],
        [2*x*z - 2*y*w,       2*y*z + 2*x*w,     1 - 2*x**2 - 2*y**2]
    ])



# Initialize cumulative rotation matrix with identity matrix (world frame)
cumulative_rotation_matrix = np.identity(3)

# File path
file_path = "C:\\Users\\Admin\\Desktop\\encode trial\\newputty.log"

# Initialize variables to store parsed data
counter = None
linear_acc = {'x': None, 'y': None, 'z': None}
quaternion = {'i': None, 'j': None, 'k': None, 'real': None}
current_time = None  # To store the parsed timestamp in microseconds

# Parsing and processing the data from the file
with open(file_path, 'r') as file:
    capture_data = None  # Tracks if we are capturing acceleration or quaternion data
    
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

        # Parse timestamp for acceleration data
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
            
            # Once all components are captured, process linear acceleration
            if linear_acc['x'] is not None and linear_acc['y'] is not None and linear_acc['z'] is not None:
                # Ensure quaternion is ready for rotation
                if quaternion['i'] is not None and quaternion['j'] is not None and quaternion['k'] is not None and quaternion['real'] is not None:
                    # Convert quaternion to rotation matrix for current orientation
                    rotation_matrix = quaternion_to_rotation_matrix(quaternion)
                    cumulative_rotation_matrix = np.dot(cumulative_rotation_matrix, rotation_matrix)
                    
                    # Rotate the local acceleration vector to align with the global frame
                    acceleration_global = np.dot(cumulative_rotation_matrix, np.array([linear_acc['x'], linear_acc['y'], linear_acc['z']]))

                    # Integrate in the global frame using timestamp-based time interval
                    if prev_time != 0:  # Ensure it's not the first iteration
                        prev_vx, prev_vy, prev_vz, prev_px, prev_py, prev_pz = trapezoidal_integration(
                            prev_time, current_time,
                            prev_ax, prev_ay, prev_az,
                            acceleration_global[0], acceleration_global[1], acceleration_global[2],
                            prev_vx, prev_vy, prev_vz,
                            prev_px, prev_py, prev_pz
                        )

                        # Store the global position (scaled to cm for visualization)
                        
                        if abs(prev_ax) <= 0.01:
                            prev_ax = 0
                        if abs(prev_ay) <= 0.01:
                            prev_ay = 0
                        if abs(prev_ax) <= 0.01:
                            prev_ax = 0
                        if abs(prev_az) <= 0.01:
                            prev_az = 0
                        
                        xvals.append(prev_px * 100)
                        yvals.append(prev_py * 100)
                        zvals.append(prev_pz * 100)

                        # Print position and quaternion for debugging
                        print(f"Counter: {counter}, Time: {current_time/1000} ms, Position: ({prev_px * 100:.2f}, {prev_py * 100:.2f}, {prev_pz * 100:.2f}), Quaternion: {quaternion}")

                    # Update time and previous accelerations
                    prev_time = current_time
                    prev_ax, prev_ay, prev_az = acceleration_global

                # Reset linear acceleration values for next capture
                linear_acc = {'x': None, 'y': None, 'z': None}
        
        elif capture_data == "Q":
            if line.startswith("i ="):
                quaternion['i'] = float(line.split("=")[1].strip())
            elif line.startswith("j ="):
                quaternion['j'] = float(line.split("=")[1].strip())
            elif line.startswith("k ="):
                quaternion['k'] = float(line.split("=")[1].strip())
            elif line.startswith("r ="):
                quaternion['real'] = float(line.split("=")[1].strip())

# Plot the path for visualization
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(xvals, yvals, zvals, label='Path')
ax.set_xlabel('X Position (cm)')
ax.set_ylabel('Y Position (cm)')
ax.set_zlabel('Z Position (cm)')
plt.legend()
plt.show()
