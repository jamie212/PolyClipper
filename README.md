# PolyClipper: An Intuitive Polygon Partitioning Library with Interactive Visualization

## Basic Information

* Project Name: PolyClipper
* Github repository url: https://github.com/jamie212/PolyClipper
* Languages: C++ (core library), Python (bindings and GUI)
* Algorithm: Ear Clipping

Polygon partitioning is a well-known problem in computational geometry. The goal is to divide a simple polygon into smaller polygons, such as triangles or convex polygons, without introducing new vertices. With the implementation of the Ear Clipping algorithm and a user-friendly Python interface, PolyClipper is perfect for computer science students, researchers, and developers working in computational geometry or related areas.

## Problem to Solve

There are various algorithms available for polygon partitioning, such as Ear Clipping and Hertel-Mehlhorn. However, implementing these algorithms and integrating them into other programming languages can be challenging.

The goal of this project is to develop a C++ library for polygon partitioning that can be easily called from Python, providing an easy-to-use API and a simple graphical user interface for visualization and testing.

## Prospective Users

The prospective users of the Polygon Partitioning Library include computer science students, researchers, and software developers working in the field of computational geometry or related areas.

## System Architecture

The PolyClipper library will be developed in C++ for the core polygon partitioning functionality. Python will be used to create bindings for the C++ code using ctypes and to develop a simple graphical user interface using Tkinter.

The system architecture of the library will consist of the following components:

* Polygon data structures (C++)
* Ear Clipping algorithm implementation (C++)
* API (C++ and Python)
* Python bindings using ctypes (Python)
* Interactive GUI for creating, partitioning and visualizing polygons (Python, Tkinter)

## API Description

The following API will be provided in C++ and Python:

* `create_polygon(vertices)` (C++): Create a polygon with given vertices
* `partition_polygon(vertices, vertex_count)` (C++): Partition a polygon into smaller polygons (e.g., triangles)
* `partition_polygon_py(input_coordinates)` (Python): Partition a polygon using Python list of vertices, internally calling the C++ `partition_polygon` function
* `get_partitioned_polygons_py()` (Python): Get the partitioned polygons in Python-friendly format


## Engineering Infrastructure

1. Automatic build system: GNU make
2. Version control: git
3. Testing framework: pytest
4. Documentation: README.md

## Schedule

* Week 1 (4/10): Study domain knowledge and Ear Clipping algorithm
* Week 2 (4/17): Design polygon data structures and functions
* Week 3 (4/24): Implement Ear Clipping algorithm in C++
* Week 4 (5/1): Implement the API functions and create Python bindings using ctypes
* Week 5 (5/8): Develop an interactive GUI using Tkinter, allowing users to draw polygons and visualize partition results
* Week 6 (5/15): Write tests and optimize the code
* Week 7 (5/22): Refine the GUI and add more features if needed
* Week 8 (5/29): Finalize the project, and prepare the presentation

## References

* Held, M. (2011). FIST: Fast Industrial-Strength Triangulation of Polygons. Algorithmica, 61(4), 964-986. 
* Li, Y., & Sun, G. (2016). A Practical Algorithm for Decomposing Polygonal Domains into Convex Polygons. Journal of Computational Information Systems, 12(5), 2037-2044. 
* Wikipedia https://en.wikipedia.org/wiki/Polygon_partition
* The Stony Brook Algorithm Repository https://algorist.com/problems/Polygon_Partitioning.html
* PolyPartition https://github.com/ivanfratric/polypartition




