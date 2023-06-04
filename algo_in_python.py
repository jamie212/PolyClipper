from math import acos, sqrt, pi
from typing import List, Tuple

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

Polygon = List[Point]

def cross_product(a: Point, b: Point, c: Point) -> float:
    ax = a.x - b.x
    ay = a.y - b.y
    bx = b.x - c.x
    by = b.y - c.y
    return ax * by - ay * bx

def dot_product(a: Point, b: Point, c: Point) -> float:
    ba_x = a.x - b.x
    ba_y = a.y - b.y
    bc_x = c.x - b.x
    bc_y = c.y - b.y
    return ba_x * bc_x + ba_y * bc_y

def norm(a: Point, b: Point) -> float:
    x = a.x - b.x
    y = a.y - b.y
    return sqrt(x * x + y * y)

def angle(a: Point, b: Point, c: Point) -> float:
    cosTheta = dot_product(a, b, c) / (norm(a, b) * norm(b, c))
    angleInRadians = acos(max(-1.0, min(1.0, cosTheta)))
    angleInDegrees = angleInRadians * 180.0 / pi
    return angleInDegrees

def is_point_in_triangle(point: Point, a: Point, b: Point, c: Point) -> bool:
    v0_x = c.x - a.x
    v0_y = c.y - a.y
    v1_x = b.x - a.x
    v1_y = b.y - a.y
    v2_x = point.x - a.x
    v2_y = point.y - a.y
    
    dot00 = v0_x * v0_x + v0_y * v0_y
    dot01 = v0_x * v1_x + v0_y * v1_y
    dot02 = v0_x * v2_x + v0_y * v2_y
    dot11 = v1_x * v1_x + v1_y * v1_y
    dot12 = v1_x * v2_x + v1_y * v2_y
    
    invDenom = 1.0 / (dot00 * dot11 - dot01 * dot01)
    u = (dot11 * dot02 - dot01 * dot12) * invDenom
    v = (dot00 * dot12 - dot01 * dot02) * invDenom
    
    return (u >= 0) and (v >= 0) and (u + v < 1)

def is_ear(poly: Polygon, a: int, b: int, c: int) -> bool:
    angleInDegrees = angle(poly[a], poly[b], poly[c])
    if angleInDegrees >= 180:
        return False

    for p in poly:
        if p.x == poly[a].x and p.y == poly[a].y:
            continue
        if p.x == poly[b].x and p.y == poly[b].y:
            continue
        if p.x == poly[c].x and p.y == poly[c].y:
            continue
        if is_point_in_triangle(p, poly[a], poly[b], poly[c]):
            return False

    crossProduct1 = cross_product(poly[a], poly[b], poly[c])
    if crossProduct1 < 0:
        return False
    return True

def orientation(p: Point, q: Point, r: Point) -> int:
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
    if val == 0:
        return 0
    return 1 if val > 0 else 2

def do_intersect(p1: Point, q1: Point, p2: Point, q2: Point) -> bool:
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)
    if o1 != o2 and o3 != o4:
        return True
    return False

def is_self_intersecting(poly: Polygon) -> bool:
    n = len(poly)
    for i in range(n):
        next_i = (i + 1) % n
        for j in range(i + 1, n):
            next_j = (j + 1) % n
            if i != j and next_i != j and i != next_j:
                if do_intersect(poly[i], poly[next_i], poly[j], poly[next_j]):
                    return True
    return False

def ear_clipping(poly: Polygon) -> List[Polygon]:
    remaining = poly.copy()
    triangles = []
    n = len(poly)
    if is_self_intersecting(poly):
        return triangles
    i = 0
    while n > 3:
        clipped = False
        for i in range(n):
            a = (i + n - 1) % n
            b = i
            c = (i + 1) % n
            if is_ear(remaining, a, b, c):
                triangles.append([remaining[a], remaining[b], remaining[c]])
                remaining.pop(i)
                clipped = True
                break
        if not clipped:
            raise RuntimeError("Failed to clip an ear.")
        n = len(remaining)
    triangles.append([remaining[0], remaining[1], remaining[2]])
    return triangles
