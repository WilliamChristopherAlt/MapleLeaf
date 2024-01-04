import matplotlib.pyplot as plt
import numpy as np, matplotlib.colors as mcolors
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt

functions2 = [
    lambda x, y: (0.8 * x + 0.1, 0.8 * y + 0.04),
    lambda x, y: (0.5 * x + 0.25, 0.5 * y + 0.4),
    lambda x, y: (0.355 * x - 0.355 * y + 0.266, 0.35 * x + 0.355 * y + 0.078),
    lambda x, y: (0.355 * x + 0.355 * y + 0.378, -0.355 * x + 0.355 * y + 0.434)
]

def draw(data, colorMode, cmapName=None):
    if colorMode == 'binary':
        cmap = 'binary'
    elif colorMode == 'grey':
        cmap_colors = [(255, 255, 255)] + [(i/255, i/255, i/255) for i in range(256)]
        cmap = mcolors.ListedColormap(cmap_colors)
    elif colorMode == 'colorful':
        # Create a custom colormap based on provided map
        custom_cmap = plt.cm.get_cmap(cmapName, 256)
        # Set the color for 0 to white
        custom_cmap_colors = custom_cmap(np.arange(custom_cmap.N))
        custom_cmap_colors[0] = [1, 1, 1, 1]  # White color
        # Create the modified colormap
        cmap = mcolors.ListedColormap(custom_cmap_colors)

    plt.imshow(data, cmap=cmap)

    plt.axis('equal')
    plt.axis('off')
    plt.tight_layout()
    # plt.savefig(r'C:\Users\PC\Downloads\vicsek.png', dpi=2000)
    plt.show()

def maple(iterations):
    # Initialize the set with a single point (0, 0)
    points = [(0.5, 0.0)]

    for _ in range(iterations):
        new_points = []
        for point in points:
            for func in functions2:
                new_points.append(func(*point))
        points = new_points

    return points

def coordinates_list_to_matrix(points, density, maxX, minX, maxY, minY):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]

    width = int((maxX - minX) * density)
    height = int((maxY - minY) * density)

    data = np.zeros((height+1, width+1), dtype=int)

    # Set elements to 1 at the indices corresponding to the complex numbers
    for x, y in zip(xs, ys):
        data[-int((y-minY)*density)][int((x-minX)*density)] += 1
        # use this if you just want a masked matrix
        # data[-int((y-minY)*density)][int((x-minX)*density)] = True

    return data

def save_image(data, file_path, colorMode='binary', cmapName=None):
    if colorMode == 'binary':
        # Convert the boolean matrix to an integer matrix (255 for False, 0 for True)
        int_data = np.where(data, 0, 255).astype(np.uint8)
    elif colorMode == 'grey' or 'colorful':
        if colorMode == 'grey':
            cmap_colors = [(1, 1, 1)] + [(i/255, i/255, i/255) for i in range(256)]
        elif colorMode == 'colorful':
            # Create a custom colormap based on provided map
            custom_cmap = plt.cm.get_cmap(cmapName, 256)
            # Set the color for 0 to white
            cmap_colors = custom_cmap(np.arange(custom_cmap.N))
            cmap_colors[0] = [1, 1, 1, 1]  # White color

        custom_cmap = mcolors.ListedColormap(cmap_colors)
        # Normalize data to range [0, 1] to match the colormap
        normalized_data = (data - np.min(data)) / (np.max(data) - np.min(data))
        # Map the normalized values to RGB values using the colormap
        rgb_data = custom_cmap(normalized_data)
        # Scale RGB values to the range [0, 255]
        int_data = (rgb_data[:, :, :3] * 255).astype(np.uint8)

    # Create an image from the RGB matrix
    image = Image.fromarray(int_data)
    image.save(file_path)

def generateAndSavePics():
    for order in range(8, 13):
        for density in [1000, 2000, 3000]:
            points = maple(order)
            data = coordinates_list_to_matrix(points, density, 1, 0, 1, 0)

            # Save the array to a file
            np.save(r"C:\Users\PC\Downloads\mapleLeafs\datas" + rf"\o{order}d{density}", data)

    for order in range(8, 13):
        for density in [1000, 2000, 3000]:
            data = np.load(r"C:\Users\PC\Downloads\mapleLeafs\datas" + rf"\o{order}d{density}.npy")

            save_image1(data, r"C:\Users\PC\Downloads\mapleLeafs\pics" + rf"\o{order}d{density}.png")

def main():
    # order = 10
    # density = 1000

    # points = maple(order)
    # data = coordinates_list_to_matrix(points, density, 1, 0, 1, 0)
    # Load the array from the file
    data = np.load(r"C:\Users\PC\Desktop\Programming\Python\Fractals\pictures\mapleLeafs\datas\o10d1000.npy")

    cmapName = 'terrain_r'
    # save_image(data, r"C:\Users\PC\Desktop\Programming\Python\Fractals\pictures\mapleLeafs" + fr"\{cmapName}.png", colorMode='colorful',
    #            cmapName=cmapName)
    draw(data, 'colorful', cmapName)

main()

