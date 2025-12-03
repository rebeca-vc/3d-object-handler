import math

def normalize(vector):
    norm = math.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)
    if norm == 0: 
        return (0, 0, 0)
    return (vector[0]/norm, vector[1]/norm, vector[2]/norm)

def dot(v1, v2):
    return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]

def sub(v1, v2):
    return (v1[0]-v2[0], v1[1]-v2[1], v1[2]-v2[2])

def add(v1, v2):
    return (v1[0]+v2[0], v1[1]+v2[1], v1[2]+v2[2])

def reflect(i, n):
    # R = I - 2.0 * dot(N, I) * N
    d = dot(n, i)
    return (i[0] - 2.0 * d * n[0],
            i[1] - 2.0 * d * n[1],
            i[2] - 2.0 * d * n[2])
def cross(a, b):
    return [
        a[1] * b[2] - a[2] * b[1],  # X = ay*bz - az*by
        a[2] * b[0] - a[0] * b[2],  # Y = az*bx - ax*bz
        a[0] * b[1] - a[1] * b[0]   # Z = ax*by - ay*bx
    ]
