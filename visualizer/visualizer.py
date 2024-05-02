import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import sys

def visualize_grid(images_directory='images/', figsize=(8, 8)):
    """
    Visualize a grid of images read from stdin.

    Args:
        images_directory (str): Directory containing the images.
        figsize (tuple): Size of the figure (width, height).
    """
    grid_str = sys.stdin.read().strip()
    rows = grid_str.split('\n')
    grid = [row.replace('\t', ' ').split() for row in rows]  # Replace tabs with spaces and then split by spaces

    num_rows = len(grid)
    num_cols = len(grid[0])

    fig, axs = plt.subplots(num_rows, num_cols, figsize=figsize)

    for i, row in enumerate(grid):
        for j, img_code in enumerate(row):
            img_code = img_code.strip()  # Remove leading/trailing whitespace
            img_path = os.path.join(images_directory, f"{img_code}.png")
            if os.path.exists(img_path):
                img = mpimg.imread(img_path)
                axs[i, j].imshow(img)
                axs[i, j].axis('off')
            else:
                print(f"Image {img_code}.png not found.")

    plt.tight_layout()
    plt.show()

visualize_grid()
