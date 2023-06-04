import sys
import matplotlib.pyplot as plt

def plot_points(input_file):
    data = []
    with open(input_file, 'r') as file:
        num_points = int(file.readline().strip())
        for _ in range(num_points):
            line = file.readline().strip().split()
            if line:
                point = [int(coord) for coord in line]
                data.append(point)

    x = [point[0] for point in data]
    y = [point[1] for point in data]

    y = [-coord for coord in y]

    plt.plot(x, y, marker='.')
    plt.plot(x, y, linestyle='-', color='black')

    plt.gca().set_aspect('equal', adjustable='box')
    plt.axis('off') 

    plt.show()


if len(sys.argv) > 1:
    input_file_path = sys.argv[1]
    plot_points(input_file_path)
else:
    print("Please provide the input file path as a command line argument.")
