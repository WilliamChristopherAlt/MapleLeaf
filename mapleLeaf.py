import matplotlib.pyplot as plt
import numpy as np, matplotlib.colors as mcolors
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import random, timeit

functions = [
    lambda x, y: (0.14*x+0.01*y-0.08, +0.00*x+0.51*y-1.31),
    lambda x, y: (0.43*x+0.52*y+1.49, -0.45*x+0.50*y-0.75),
    lambda x, y: (0.45*x-0.49*y-1.62, 0.47*x+0.47*y-0.74),
    lambda x, y: (0.49*x+0.00*y+0.02, 0.00*x+0.51*y+1.62)
]

def draw(data):
    # cmap_colors = [(25, 25, 25)] + [(i/255, i/255, i/255) for i in range(256)]
    # custom_cmap = mcolors.ListedColormap(cmap_colors)
    # plt.imshow(data, cmap=custom_cmap)
    plt.imshow(data, cmap='binary')
    plt.axis('equal')
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def maple(iterations):
    xs = np.empty(iterations + 1)
    ys = np.empty(iterations + 1)
    xs[0] = 2
    ys[0] = 2

    cumulative_prob = np.cumsum([0.1, 0.35, 0.35, 0.2])

    for i in range(1, iterations):
        r = random.random()
        index = np.searchsorted(cumulative_prob, r)
        xs[i], ys[i] = functions[index](xs[i-1], ys[i-1])

    return xs, ys

def coordinates_list_to_matrix(xs, ys, density, maxX, minX, maxY, minY):
    width = int((maxX - minX) * density)
    height = int((maxY - minY) * density)
    data = np.zeros((height, width), dtype=int)
    # Set elements to 1 at the indices corresponding to the complex numbers
    for x, y in zip(xs, ys):
        # data[-int((y-minY)*density)][int((x-minX)*density)] += 1
        # use this if you just want a masked matrix
        data[-int((y-minY)*density)][int((x-minX)*density)] = True
    return data

def save_image(data, file_path):
    # Convert the boolean matrix to an integer matrix (255 for False, 0 for True)
    int_data = np.where(data, 0, 255).astype(np.uint8)
    # Create an image from the integer matrix
    image = Image.fromarray(int_data)
    # Save the image
    image.save(file_path)

def save_image1(data, file_path):
    cmap_colors = [(1, 1, 1)] + [(i/255, i/255, i/255) for i in range(256)]
    custom_cmap = mcolors.ListedColormap(cmap_colors)

    # Normalize data to range [0, 1] to match the colormap
    normalized_data = (data - np.min(data)) / (np.max(data) - np.min(data))

    # Map the normalized values to RGB values using the colormap
    rgb_data = custom_cmap(normalized_data)

    # Scale RGB values to the range [0, 255]
    int_data = (rgb_data[:, :, :3] * 255).astype(np.uint8)

    # Create an image from the RGB matrix
    image = Image.fromarray(int_data)

    # Save the image
    image.save(file_path)

def main():
    iterations = 200000
    density = 75

    xs, ys = maple(iterations)
    data = coordinates_list_to_matrix(xs, ys, density, 4, -4, 4, -4)
    
    # save_image1(data, r"C:\Users\PC\Downloads\maple2.png")
    draw(data)

main()