import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata  # Add this line to fix the error

# Load the data from CSV
data = pd.read_csv("summary_last_50_means.csv")

# Ensure 'X', 'Y', and some parameters are present in the data
if 'X' in data.columns and 'Y' in data.columns:
    available_columns = [col for col in data.columns if col not in ['X', 'Y', 'Location']]

    print("Available parameters to plot:")
    for idx, col in enumerate(available_columns):
        print(f"{idx + 1}. {col}")

    # Ask user to select parameters for multiple plots
    selected_params = input("Enter the numbers of the parameters to plot (comma-separated, e.g., 1,2,3): ")
    selected_indices = [int(i.strip()) - 1 for i in selected_params.split(',')]
    
    selected_columns = [available_columns[i] for i in selected_indices]

    # Set up the subplot grid
    num_plots = len(selected_columns)
    rows = (num_plots + 1) // 2  # Two columns per row
    cols = 2 if num_plots > 1 else 1

    fig, axes = plt.subplots(rows, cols, figsize=(14, 6 * rows))
    axes = axes.flatten()  # Flatten the axes array for easy iteration

    for i, param in enumerate(selected_columns):
        # Extract the X, Y, and parameter values
        x = data['X']
        y = data['Y']
        z = data[param]

        # Create grid data for contour plot
        grid_x, grid_y = np.mgrid[min(x):max(x):100j, min(y):max(y):100j]
        grid_z = griddata((x, y), z, (grid_x, grid_y), method='cubic')

        # Plot each graph in the subplot
        contour = axes[i].contourf(grid_x, grid_y, grid_z, cmap='coolwarm')
        fig.colorbar(contour, ax=axes[i], label=param)
        axes[i].set_title(f'Contour Map of {param}')
        axes[i].set_xlabel('X Coordinate')
        axes[i].set_ylabel('Y Coordinate')
        axes[i].grid(visible=True, which='both', linestyle='--', alpha=0.7)

    # Hide any unused subplots
    for j in range(num_plots, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()

else:
    print("Ensure the CSV contains 'X', 'Y', 'Location' and other data columns.")
