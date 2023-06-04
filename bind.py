import optimal_algo

# Open the file
with open('input4.txt', 'r') as file:
    # Read the first line to get the number of points
    num_points = int(file.readline().strip())
    
    # Create a Polygon
    polygon = []
    
    # Read each subsequent line to get the points
    for _ in range(num_points):
        # Each line should be in the format "x y"
        line = file.readline().strip()
        x, y = map(float, line.split())
        
        point = algo.Point()
        point.x = x
        point.y = y
        polygon.append(point)

# Perform ear clipping
triangles = algo.ear_clipping(polygon)
if not triangles:
    print("intersect")

# # Print the result
# for triangle in triangles:
#     for point in triangle:
#         print(f'({point.x}, {point.y})')
#     print()

with open('output3.txt', 'w') as file:
    # Write the number of triangles
    file.write(str(len(triangles)) + '\n')

    # Write each triangle
    for triangle in triangles:
        for point in triangle:
            file.write(f'{point.x} {point.y}\n')
        file.write('\n')