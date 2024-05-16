import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import sys
from PIL import Image
import numpy as np

VOID_CODE_LENGTH = 1
IDK_CODE_LENGTH = 5

O_UP = np.uint8(0)
O_DOWN = np.uint8(1)
O_LEFT = np.uint8(2)
O_RIGHT = np.uint8(3)
O_HORIZONTAL = np.uint8(4)
O_VERTICAL = np.uint8(5)

T_LOCK = np.uint8(6)
T_JUNCTION = np.uint8(7)
T_TURN = np.uint8(8)
T_CONNECTION = np.uint8(9)

NORMAL = 1
LIMITADO = 2
NAO_LIMITADO = 4

def str_from_orientation(orientation):
    if orientation == O_UP:
        return 'C'
    elif orientation == O_DOWN:
        return 'B'
    elif orientation == O_LEFT:
        return 'E'
    elif orientation == O_RIGHT:
        return 'D'
    elif orientation == O_HORIZONTAL:
        return 'H'
    elif orientation == O_VERTICAL:
        return 'V'

def orientations_from_bin(bin):
    if bin == 0b0000:
        return np.array([], dtype=np.uint8)
    elif bin == 0b1000:
        return np.array([O_UP], dtype=np.uint8)
    elif bin == 0b0100:
        return np.array([O_LEFT], dtype=np.uint8)
    elif bin == 0b0010:
        return np.array([O_RIGHT], dtype=np.uint8)
    elif bin == 0b0001:
        return np.array([O_DOWN], dtype=np.uint8)
    elif bin == 0b0110:
        return np.array([O_LEFT, O_RIGHT], dtype=np.uint8)
    elif bin == 0b1010:
        return np.array([O_UP, O_RIGHT], dtype=np.uint8)
    elif bin == 0b0011:
        return np.array([O_RIGHT, O_DOWN], dtype=np.uint8)
    elif bin == 0b1100:
        return np.array([O_UP, O_LEFT], dtype=np.uint8)
    elif bin == 0b0101:
        return np.array([O_LEFT, O_DOWN], dtype=np.uint8)
    elif bin == 0b1001:
        return np.array([O_UP, O_DOWN], dtype=np.uint8)
    elif bin == 0b0111:
        return np.array([O_LEFT, O_RIGHT, O_DOWN], dtype=np.uint8)
    elif bin == 0b1011:
        return np.array([O_UP, O_RIGHT, O_DOWN], dtype=np.uint8)
    elif bin == 0b1101:
        return np.array([O_UP, O_LEFT, O_DOWN], dtype=np.uint8)
    elif bin == 0b1110:
        return np.array([O_UP, O_LEFT, O_RIGHT], dtype=np.uint8)
    elif bin == 0b1111:
        return np.array([O_UP, O_LEFT, O_RIGHT, O_DOWN], dtype=np.uint8)


def str_from_type(piece_type):
    if piece_type == T_LOCK:
        return 'F'
    elif piece_type == T_JUNCTION:
        return 'B'
    elif piece_type == T_TURN:
        return 'V'
    elif piece_type == T_CONNECTION:
        return 'L'

import numpy as np
from PIL import Image

LIMITADO = "LIMITADO"
NAO_LIMITADO = "NAO_LIMITADO"

import numpy as np
from PIL import Image

LIMITADO = "LIMITADO"
NAO_LIMITADO = "NAO_LIMITADO"

def load_image(img_path, color):
    try:
        imagem = Image.open(img_path)
        imagem_array = np.array(imagem)

        if color == LIMITADO:
            high_intensity_pixels = np.all((imagem_array > 200) & (imagem_array <= 255), axis=-1)
            new_color = np.array([255, 183, 55, 50]) 
            imagem_array[high_intensity_pixels] = np.ones_like(imagem_array[high_intensity_pixels]) * new_color

        elif color == NAO_LIMITADO:
            high_intensity_pixels = np.all((imagem_array > 200) & (imagem_array <= 255), axis=-1)
            new_color = np.array([50, 50, 50, 255])
            imagem_array[high_intensity_pixels] = np.ones_like(imagem_array[high_intensity_pixels]) * new_color
        
        elif color == NORMAL:
            high_intensity_pixels = np.all((imagem_array > 200) & (imagem_array <= 255), axis=-1)
            new_color = np.array([0, 100, 0, 255])
            imagem_array[high_intensity_pixels] = np.ones_like(imagem_array[high_intensity_pixels]) * new_color

        return Image.fromarray(imagem_array)

    except FileNotFoundError:
        print(f"Image {img_path} not found.")
        return None





def visualize_grid(images_directory='images/', figsize=(8, 8)):
    """
    Visualize a grid of images.

    Args:
        images_directory (str): Directory containing the images.
        figsize (tuple): Size of the figure (width, height).
    """
    grid_str = sys.stdin.read().strip()
    rows = grid_str.split('\n')
    grid = [row.replace('\t', ' ').split() for row in rows]

    processed_grid = grid
    
    '''
    for row in grid:
        processed_row = []
        for element in row:
            if len(element) == VOID_CODE_LENGTH:
                processed_row.append("void")
            elif len(element) == IDK_CODE_LENGTH:
                processed_row.append("idk")
            else:
                processed_row.append(element)
        processed_grid.append(processed_row)
    '''

    num_rows = len(processed_grid)
    num_cols = len(processed_grid[0])

    fig, axs = plt.subplots(num_rows, num_cols, figsize=figsize)
    for i, row in enumerate(processed_grid):
        for j, img_code in enumerate(row):
            img_code = img_code.strip()  # Remove leading/trailing whitespace
            if len(img_code) == 2:
                cor = NORMAL
            elif len(img_code) == 5:
                    bin1 = int(img_code[1:], 2)
                    img_code = img_code[0] + str_from_orientation(orientations_from_bin(bin1)[0])
                    cor = LIMITADO
            elif len(img_code) == 6:
                bin1 = int(img_code[2:], 2)
                img_code = img_code[0]

                if img_code[0] == "L":
                    img_code += "V"
                else:
                    img_code += "C"

                cor = NAO_LIMITADO

            img_path = os.path.join(images_directory, f"{img_code}.png")
            if os.path.exists(img_path):
                img = load_image(img_path, cor)
                if img is not None:
                    axs[i, j].imshow(img)
                    axs[i, j].axis('off')
            else:
                print(f"Image {img_code}.png not found.")

    plt.tight_layout()
    plt.show()

visualize_grid()
