import numpy as np
from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Function to create a homogeneous transformation matrix
def create_homogeneous_matrix(rotation_matrix, translation_vector):
    # Ensure translation_vector is a NumPy array to allow reshaping
    translation_vector = np.array(translation_vector)
    homogeneous_matrix = np.concatenate((rotation_matrix, translation_vector.reshape(3, 1)), axis=1)
    homogeneous_matrix = np.vstack((homogeneous_matrix, np.array([0, 0, 0, 1])))
    return homogeneous_matrix

def trapezoidal_integration(prev_time, current_time, prev_ax, prev_ay, prev_az, 
                            current_ax, current_ay, current_az,
                            prev_vx, prev_vy, prev_vz,
                            prev_px, prev_py, prev_pz):
    dt = (current_time - prev_time) / 1000000  # convert milliseconds to seconds

    # Velocity
    new_vx = prev_vx + 0.5 * (prev_ax + current_ax) * dt
    new_vy = prev_vy + 0.5 * (prev_ay + current_ay) * dt
    new_vz = prev_vz + 0.5 * (prev_az + current_az) * dt

    # Position
    new_px = prev_px + 0.5 * (prev_vx + new_vx) * dt
    new_py = prev_py + 0.5 * (prev_vy + new_vy) * dt
    new_pz = prev_pz + 0.5 * (prev_vz + new_vz) * dt
    
    return new_vx, new_vy, new_vz, new_px, new_py, new_pz


# Function to calculate translations from acceleration data and timestamps
def calculate_translations(acceleration, timestamp):
    translations = []  # To store the position values
    velocity = [0.0, 0.0, 0.0]  # Initial velocity (vx, vy, vz)
    position = [0.0, 0.0, 0.0]  # Initial position (px, py, pz)

    # Loop through each timestamped acceleration
    for i in range(1, len(acceleration)):
        # Previous and current timestamps
        prev_time, current_time = timestamp[i - 1], timestamp[i]

        # Previous and current accelerations
        prev_acc = acceleration[i - 1]
        current_acc = acceleration[i]

        # Apply trapezoidal integration
        new_vx, new_vy, new_vz, new_px, new_py, new_pz = trapezoidal_integration(
            prev_time, current_time,
            prev_acc[0], prev_acc[1], prev_acc[2],
            current_acc[0], current_acc[1], current_acc[2],
            velocity[0], velocity[1], velocity[2],
            position[0], position[1], position[2]
        )

        # Update velocity and position for the next iteration
        velocity = [new_vx, new_vy, new_vz]
        position = [new_px, new_py, new_pz]

        # Append the new position to the list
        translations.append(position)

    return translations



# File path
file_path = "C:\\Users\\Admin\\Desktop\\encode trial\\newputty.log"

# Initialize variables to store parsed data
counter = None
linear_acc = {'x': None, 'y': None, 'z': None}
quaternion = {'i': None, 'j': None, 'k': None, 'real': None}
current_time = None

# Lists to store parsed data
quaternions = []
acceleration = []
timestamp = []  # In milliseconds

# Process the file and store parsed data in lists
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
                linear_acc['z'] = 0
            
            # Check if all linear acceleration components are captured
            if None not in linear_acc.values() and current_time is not None:
                # Store acceleration and timestamp
                acceleration.append([linear_acc['x'], linear_acc['y'], linear_acc['z']])
                timestamp.append(current_time)  
                
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

            # Check if quaternion is fully captured and store it
            if None not in quaternion.values():
                quaternions.append([quaternion['i'], quaternion['j'], quaternion['k'], quaternion['real']])
                
                # Reset values for the next quaternion capture
                quaternion = {'i': None, 'j': None, 'k': None, 'real': None}

# Output results for debugging
print("Quaternions:", quaternions)
print("Acceleration:", acceleration)
print("Timestamps (ms):", timestamp)


# Calculate translations based on provided acceleration and timestamp data
translations = calculate_translations(acceleration, timestamp)

# Output results
print("Calculated translations:", translations)
    
# Convert quaternions to rotation matrices
rotation_matrices = [R.from_quat(q).as_matrix() for q in quaternions]

# Initialize the list to store cumulative transformation matrices
transformation_matrices = []

print(len(rotation_matrices),len(translations))
#Removing last read value in case of size differences in data
if len(rotation_matrices) > len(translations):
    rotation_matrices = rotation_matrices[1:]
elif len(translations) > len(rotation_matrices):
    translations = translations[1:]
    

# Initial transformation is identity (from frame 0 to frame 0)
current_transformation = np.identity(4)
transformation_matrices.append(current_transformation)

# Oscar transformation logic

# Iterate over each frame to calculate cumulative transformations
for i in range(len(rotation_matrices)):
    # Calculate the transformation from the previous frame to the current frame
    if i == 0:
        rotation_relative = rotation_matrices[i]
    else:
        # Relative rotation: current rotation relative to the last frame
        rotation_relative = np.dot(np.transpose(rotation_matrices[i - 1]), rotation_matrices[i])
    
    translation_relative = translations[i]  # Translation for the current frame
    transformation_relative = create_homogeneous_matrix(rotation_relative, translation_relative)
    
    # Update the cumulative transformation matrix
    current_transformation = np.dot(current_transformation, transformation_relative)
    transformation_matrices.append(current_transformation)



# Display the global displacement vector from t0 to each frame in the global coordinate system
print("Global displacement vectors for each frame in the global coordinate system:")
for i, matrix in enumerate(transformation_matrices, start=0):
    displacement_vector = matrix[:3, 3]  # Extract the translation component
    print(f"Displacement vector for frame {i} in global coordinates: {displacement_vector}")
    print(transformation_matrices[i])


# Assuming `translations` is already computed and available
def plot_translations(translations):
    """
    Plots the 3D line path of calculated translations.
    
    Parameters:
    translations (list of lists): List of [x, y, z] displacement vectors in global coordinates.
    """
    # Separate translations into x, y, and z components
    x_vals, y_vals, z_vals = zip(*translations)

    # Plot the 3D line path
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x_vals, y_vals, z_vals, label='Calculated Path', color='blue', marker='o', markersize=4, linewidth=1)
    
    # Mark the start and end points
    ax.scatter(x_vals[0], y_vals[0], z_vals[0], color='green', s=50, label='Start')
    ax.scatter(x_vals[-1], y_vals[-1], z_vals[-1], color='red', s=50, label='End')

    # Set labels and title
    ax.set_xlabel('X Position (m)')
    ax.set_ylabel('Y Position (m)')
    ax.set_zlabel('Z Position (m)')
    ax.set_title('3D Path of Calculated Translations')
    plt.legend()
    plt.show(block = True)


# Example usage:
plot_translations(translations)