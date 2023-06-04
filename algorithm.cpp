#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

struct Point {
    int x, y;
};

using Polygon = std::vector<Point>;

///// EAR CLIPPING /////
double crossProduct(const Point& a, const Point& b, const Point& c) {
    double ax = a.x - b.x;
    double ay = a.y - b.y;
    double bx = b.x - c.x;
    double by = b.y - c.y;

    return ax * by - ay * bx;
}

double dotProduct(const Point& a, const Point& b, const Point& c) {
    double ba_x = a.x - b.x;
    double ba_y = a.y - b.y;
    double bc_x = c.x - b.x;
    double bc_y = c.y - b.y;

    return ba_x * bc_x + ba_y * bc_y;
}

double norm(const Point& a, const Point& b) {
    double x = a.x - b.x;
    double y = a.y - b.y;

    return sqrt(x * x + y * y);
}

double angle(const Point& a, const Point& b, const Point& c) {
    double cosTheta = dotProduct(a, b, c) / (norm(a, b) * norm(b, c));
    double angleInRadians = acos(std::max(-1.0, std::min(1.0, cosTheta)));
    double angleInDegrees = angleInRadians * 180.0 / M_PI;

    return angleInDegrees;
}

bool isPointInTriangle(const Point& point, const Point& a, const Point& b, const Point& c) {
    // Compute vectors
    double v0_x = c.x - a.x;
    double v0_y = c.y - a.y;
    double v1_x = b.x - a.x;
    double v1_y = b.y - a.y;
    double v2_x = point.x - a.x;
    double v2_y = point.y - a.y;
    
    // Compute dot products
    double dot00 = v0_x * v0_x + v0_y * v0_y;
    double dot01 = v0_x * v1_x + v0_y * v1_y;
    double dot02 = v0_x * v2_x + v0_y * v2_y;
    double dot11 = v1_x * v1_x + v1_y * v1_y;
    double dot12 = v1_x * v2_x + v1_y * v2_y;
    
    // Compute barycentric coordinates
    double invDenom = 1.0 / (dot00 * dot11 - dot01 * dot01);
    double u = (dot11 * dot02 - dot01 * dot12) * invDenom;
    double v = (dot00 * dot12 - dot01 * dot02) * invDenom;
    
    return (u >= 0) && (v >= 0) && (u + v < 1);
}

bool isEar(const Polygon& poly, int a, int b, int c) {
    double angleInDegrees = angle(poly[a], poly[b], poly[c]);
    if (angleInDegrees >= 180){
        return false;
    }

    for (const auto& p : poly) {
        if (p.x == poly[a].x && p.y == poly[a].y) continue;
        if (p.x == poly[b].x && p.y == poly[b].y) continue;
        if (p.x == poly[c].x && p.y == poly[c].y) continue;

        if (isPointInTriangle(p, poly[a], poly[b], poly[c])) {
            return false;
        }
    }

    double crossProduct1 = crossProduct(poly[a], poly[b], poly[c]);

    if (crossProduct1 < 0) {
        return false;
    }
    
    return true;
}


int orientation(const Point &p, const Point &q, const Point &r) {
    double val = (q.y - p.y) * (r.x - q.x) -
                 (q.x - p.x) * (r.y - q.y);

    if (val == 0) return 0;
    return (val > 0)? 1: 2;  
}

bool doIntersect(Point p1, Point q1, Point p2, Point q2) {
    int o1 = orientation(p1, q1, p2);
    int o2 = orientation(p1, q1, q2);
    int o3 = orientation(p2, q2, p1);
    int o4 = orientation(p2, q2, q1);

    if (o1 != o2 && o3 != o4)
        return true;

    return false; 
}

bool isSelfIntersecting(const Polygon& poly) {
    int n = poly.size();
    for(int i = 0; i < n; i++) {
        int next_i = (i + 1) % n;
        for(int j = i + 1; j < n; j++) {
            int next_j = (j + 1) % n;
            if(i != j && next_i != j && i != next_j) {
                if(doIntersect(poly[i], poly[next_i], poly[j], poly[next_j])) {
                    return true;
                }
            }
        }
    }
    return false;
}

std::vector<Polygon> earClipping(const Polygon& poly) {
    Polygon remaining = poly;
    std::vector<Polygon> triangles;
    size_t n = poly.size();
    if(isSelfIntersecting(poly)) {
        return triangles;
    }
    size_t i = 0;
    while (n > 3) {
        
        bool clipped = false;
        for (; i < n; ++i) {
            
            size_t a = (i + n - 1) % n;
            size_t b = i;
            size_t c = (i + 1) % n;

            if (isEar(remaining, a, b, c)) {
                triangles.push_back({remaining[a], remaining[b], remaining[c]});
                remaining.erase(remaining.begin() + i);
                clipped = true;
                break;
            }
        }

        if (!clipped) {
            throw std::runtime_error("Failed to clip an ear.");
        }
        n = remaining.size();
        i = 0;
    }

    triangles.push_back({remaining[0], remaining[1], remaining[2]});
   
    return triangles;
}

///// OPTIMAL EDGE TRIANGLE /////
using Polygons = std::vector<Polygon>;

double dist(Point a, Point b) {
    double dx = a.x - b.x;
    double dy = a.y - b.y;
    return sqrt(dx * dx + dy * dy);
}

double cost(int i, int j, int k, std::vector<Point> &points) {
    Point p1 = points[i], p2 = points[j], p3 = points[k];
    return dist(p1, p2) + dist(p2, p3) + dist(p3, p1);
}

void retrieveTriangles(int i, int j, std::vector<std::vector<int>> &backtrack, std::vector<Point> &points, Polygons &triangles) {
    if(j <= i + 1)
        return;
    int k = backtrack[i][j];
    
    Polygon triangle = {points[i], points[k], points[j]};
    triangles.push_back(triangle);
    
    retrieveTriangles(i, k, backtrack, points, triangles);
    retrieveTriangles(k, j, backtrack, points, triangles);
}

Polygons optimalTriangulation(std::vector<Point> &points) {
    int n = points.size();

    std::vector<std::vector<double>> dp(n, std::vector<double>(n, 0));
    std::vector<std::vector<int>> backtrack(n, std::vector<int>(n, -1));
    Polygons triangles;

    for(int gap = 0; gap < n; gap++) {
        for(int i = 0, j = gap; j < n; i++, j++) {
            if(j < i+2)
                dp[i][j] = 0;
            else {
                dp[i][j] = std::numeric_limits<double>::max();
                for (int k = i+1; k<j; k++) {
                    double val = dp[i][k] + dp[k][j] + cost(i, j, k, points);
                    if(dp[i][j] > val) {
                        dp[i][j] = val;
                        backtrack[i][j] = k;
                    }
                }
            }
        }
    }

    retrieveTriangles(0, n-1, backtrack, points, triangles);

    return triangles;
}



PYBIND11_MODULE(algorithm, m) {
    py::class_<Point>(m, "Point")
        .def(py::init<>())
        .def_readwrite("x", &Point::x)
        .def_readwrite("y", &Point::y);
    
    m.def("ear_clipping", &earClipping, "A function which performs ear clipping triangulation on a polygon");
    m.def("optimal_triangulation", &optimalTriangulation, "A function which performs optimal triangulation on a polygon");

}
