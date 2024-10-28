import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Set up 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_zlim(-10, 10)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title("Real-Time 3D Trajectory")

# Initialize lists to store trajectory data
x_vals, y_vals, z_vals = [], [], []

# Animation function
def animate(i):
    # Generate random values (replace with real IMU data)
    x = np.random.uniform(-4, 4) + (x_vals[-1] if x_vals else 0)
    y = np.random.uniform(-4, 4) + (y_vals[-1] if y_vals else 0)
    z = np.random.uniform(-4, 4) + (z_vals[-1] if z_vals else 0)
    
    # Append new points to lists
    x_vals.append(x)
    y_vals.append(y)
    z_vals.append(z)

    # Clear and plot the updated trajectory
    ax.cla()
    ax.set_xlim(-20, 20)
    ax.set_ylim(-20, 20)
    ax.set_zlim(-20, 20)
    
    ax.plot3D(x_vals, y_vals, z_vals, 'red')

# Create animation
ani = FuncAnimation(fig, animate, interval=500)
plt.show()
