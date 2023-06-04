import sys
import matplotlib.pyplot as plt

def plot_triangles(input_file):
    with open(input_file, 'r') as file:
        num_triangles = int(file.readline())
        for i in range(num_triangles):

            triangle_points = []

            for _ in range(3):
                line = file.readline().strip()

                x, y = map(int, line.split())
                y = -y
                
                triangle_points.append((x, y))

            file.readline()
            
            triangle_points.append(triangle_points[0])
            
            x_coords, y_coords = zip(*triangle_points)
            
            plt.plot(x_coords, y_coords, color='black')    

    plt.gca().set_aspect('equal', adjustable='box')
    plt.axis('off') 
    plt.show()

if len(sys.argv) > 1:
    input_file_path = sys.argv[1]
    plot_triangles(input_file_path)
else:
    print("Please provide the input file path as a command line argument.")
