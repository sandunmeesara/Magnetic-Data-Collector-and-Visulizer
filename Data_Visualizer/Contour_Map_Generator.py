import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

# Load the mean data from CSV
data = pd.read_csv("summary_last_50_means.csv")

# Check if 'X', 'Y' columns exist in the data
if 'X' in data.columns and 'Y' in data.columns:
    # List all available columns for user selection
    available_columns = [col for col in data.columns if col not in ['X', 'Y', 'Location']]
    
    print("Available parameters to plot:")
    for idx, col in enumerate(available_columns):
        print(f"{idx + 1}. {col}")

    # Ask user to select a parameter by entering its number
    try:
        choice = int(input("Enter the number of the parameter to plot (e.g., 1, 2, etc.): "))
        parameter = available_columns[choice - 1]
    except (IndexError, ValueError):
        print("Invalid selection. Please enter a valid number.")
        exit()

    # Extract coordinates and the selected parameter
    x = data['X']
    y = data['Y']
    z = data[parameter]

    # Create grid data for the contour plot
    grid_x, grid_y = np.mgrid[min(x):max(x):100j, min(y):max(y):100j]
    grid_z = griddata((x, y), z, (grid_x, grid_y), method='cubic')

    # Plot the contour map
    plt.figure(figsize=(10, 8))
    contour = plt.contourf(grid_x, grid_y, grid_z, cmap='coolwarm')
    plt.colorbar(contour, label=parameter)

    # Add labels and title
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title(f'Contour Map of {parameter}')

    # Set x-ticks and y-ticks to increments of 1
    x_ticks = np.arange(int(min(x)), int(max(x)) + 1, 1)
    y_ticks = np.arange(int(min(y)), int(max(y)) + 1, 1)
    plt.xticks(x_ticks)
    plt.yticks(y_ticks)

    # Adjust plot limits to ensure points at edges are visible
    plt.xlim(min(x) - 1, max(x) + 1)
    plt.ylim(min(y) - 1, max(y) + 1)

    # Enable grid for both x and y axes
    plt.grid(visible=True, which='both', linestyle='--', color='gray', alpha=0.7)

    # Plot data points and add labels with offsets
    for idx, row in data.iterrows():
        location = row['Location']  # Ensure 'Location' column exists in the CSV
        x_coord, y_coord = row['X'], row['Y']
        value = row[parameter]

        # Extract the number from the location string (e.g., "data_location_11" -> "11")
        label_number = ''.join(filter(str.isdigit, location))
        
        # Combine the location number and the parameter value in the label
        label_text = f"{label_number} ({value:.2f})"
        
        # Plot the point with reduced marker size and gray color
        plt.plot(x_coord, y_coord, marker='o', color='black', markersize=0.5)

        # Add the label next to the point with slight offsets and gray color
        plt.text(x_coord + 0.1, y_coord + 0.1, label_text, color='black', fontsize=5, weight='bold')

    # Show the plot
    plt.show()

else:
    print("Ensure the CSV contains 'X', 'Y', and 'Location' columns.")
