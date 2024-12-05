import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def visualize_saved_figures(folder_path, images_per_row=3):
    # Get all image files in the folder (supports common formats)
    valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.svg')
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(valid_extensions)]

    if not image_files:
        print("No images found in the specified folder.")
        return

    # Calculate number of rows needed
    num_images = len(image_files)
    rows = (num_images + images_per_row - 1) // images_per_row  # Round up

    # Create a figure to hold subplots with increased size
    fig, axes = plt.subplots(rows, images_per_row, figsize=(16, 10 * rows))  # Larger figure size

    # Flatten axes array if there's more than one row
    axes = axes.flatten() if num_images > 1 else [axes]

    for i, image_file in enumerate(image_files):
        # Load the image
        img_path = os.path.join(folder_path, image_file)
        img = mpimg.imread(img_path)

        # Display the image in the subplot
        axes[i].imshow(img)
        axes[i].axis('off')  # Hide axes for a cleaner look

    # Hide any remaining empty subplots
    for j in range(num_images, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()

# Usage example
folder_path = "./Data_Sets/Data_Set_1_2024_12_04/Figures/"  # Replace with the path to your folder with images
visualize_saved_figures(folder_path)
