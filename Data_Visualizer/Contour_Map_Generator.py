import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

# Load the mean data from CSV
data = pd.read_csv("summary_last_50_means.csv")

# Ensure columns like 'X', 'Y', and 'MagneticIntensity' exist in your data
if 'X' in data.columns and 'Y' in data.columns and 'MagneticIntensity' in data.columns:
    # Extract coordinates and values
    x = data['X']
    y = data['Y']
    z = data['MagneticIntensity']

    # Create grid data for the contour plot
    grid_x, grid_y = np.mgrid[min(x):max(x):100j, min(y):max(y):100j]
    grid_z = griddata((x, y), z, (grid_x, grid_y), method='cubic')

    # Plot the contour map
    plt.figure(figsize=(10, 8))
    contour = plt.contourf(grid_x, grid_y, grid_z, cmap='viridis')
    plt.colorbar(contour, label='Magnetic Intensity')

    # Add labels and title
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Contour Map of Magnetic Intensity')

    # Set x-ticks and y-ticks to increments of 1
    x_ticks = np.arange(int(min(x)), int(max(x)) + 1, 1)
    y_ticks = np.arange(int(min(y)), int(max(y)) + 1, 1)
    plt.xticks(x_ticks)
    plt.yticks(y_ticks)

    # Enable grid for both x and y axes
    plt.grid(visible=True, which='both', linestyle='--', color='gray', alpha=0.7)

    # Show the plot
    plt.show()

else:
    print("Ensure the CSV contains 'X', 'Y', and 'MagneticIntensity' columns.")
