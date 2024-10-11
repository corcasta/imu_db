import serial
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

BAUDRATE = 115200
PORT = "/dev/ttyACM0"
quiver_objects = []

# Function to convert quaternion to rotation matrix
def quaternion_to_rotation_matrix(q):
    w, x, y, z = q
    return np.array([
        [1 - 2*y**2 - 2*z**2, 2*x*y - 2*z*w,     2*x*z + 2*y*w],
        [2*x*y + 2*z*w,       1 - 2*x**2 - 2*z**2, 2*y*z - 2*x*w],
        [2*x*z - 2*y*w,       2*y*z + 2*x*w,     1 - 2*x**2 - 2*y**2]
    ])

# Function to render an axis frame in real-time given a quaternion
def render_axis_frame(quaternion, ax):
    global quiver_objects
    
    # Convert quaternion to rotation matrix
    rotation_matrix = quaternion_to_rotation_matrix(quaternion)

    # Define the unit axes
    x_axis = np.array([1, 0, 0])
    y_axis = np.array([0, 1, 0])
    z_axis = np.array([0, 0, 1])

    # Rotate the axes using the rotation matrix
    rotated_x = np.dot(rotation_matrix, x_axis)
    rotated_y = np.dot(rotation_matrix, y_axis)
    rotated_z = np.dot(rotation_matrix, z_axis)

    # Remove the previous quiver objects if they exist
    for quiver in quiver_objects:
        quiver.remove()
    
    # Clear the list after removing
    quiver_objects.clear()

    # Plot the rotated axes with updated data
    origin = np.array([0, 0, 0])
    quiver_x = ax.quiver(*origin, *rotated_x, color='r', label="X-axis")
    quiver_y = ax.quiver(*origin, *rotated_y, color='g', label="Y-axis")
    quiver_z = ax.quiver(*origin, *rotated_z, color='b', label="Z-axis")
    
    # Store the new quiver objects to remove them in the next update
    quiver_objects = [quiver_x, quiver_y, quiver_z]

    plt.draw()
    #plt.pause(0.001)  # Small pause for real-time update

def main():
    # Set up the plot outside the function to avoid re-creating the window
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Set up the plot limits and labels
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    arduino = serial.Serial(PORT, BAUDRATE)
    
    while True:
        msg = arduino.readline()
        decoded_msg = str(msg.decode("utf-8"))
        q_components_raw = decoded_msg.split(",")
        print(f"{q_components_raw=}")
        if len(q_components_raw) == 4:
            w_raw, i_raw, j_raw, k_raw = q_components_raw 
            w = float(w_raw.split(":")[1])
            i = float(i_raw.split(":")[1])
            j = float(j_raw.split(":")[1])
            k = float(k_raw.split(":")[1][:-2])
            #print(f"{w=}, {i=}, {j=}, {k=}")
        
            render_axis_frame([w,i,j,k], ax)
            plt.pause(0.001)  # Simulate a delay (for demonstration)




if __name__ == "__main__":
    main()