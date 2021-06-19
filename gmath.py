import math
from display import *

# IMPORANT NOTE

# Ambient light is represeneted by a color value

# Point light sources are 2D arrays of doubles.
#      - The fist index (LOCATION) represents the vector to the light.
#      - The second index (COLOR) represents the color.

# Reflection constants (ka, kd, ks) are represened as arrays of
# doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

# lighting functions


def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect):
    normalize(light[LOCATION])
    # Ltest = light[LOCATION]
    normalize(normal)
    normalize(view)

    ambient = calculate_ambient(ambient, areflect)
    diffuse = calculate_diffuse(light, dreflect, normal)
    specular = calculate_specular(light, sreflect, view, normal)

    return limit_color([ambient[i] + diffuse[i] + specular[i] for i in range(3)])


def calculate_ambient(alight, areflect):
    return limit_color([areflect[i] * alight[i] for i in range(3)])


def calculate_diffuse(light, dreflect, normal):
    # L = normalize(light[LOCATION])
    # N = normalize(normal)

    cTheta = dot_product(normal, light[LOCATION])

    r = light[COLOR][0] * dreflect[0] * cTheta
    g = light[COLOR][1] * dreflect[1] * cTheta
    b = light[COLOR][2] * dreflect[2] * cTheta

    return limit_color([r, g, b])


def calculate_specular(light, sreflect, view, normal):
    # L = normalize(light[LOCATION])
    # N = normalize(normal)
    # V = normalize(view)

    c = 2 * dot_product(normal, light[LOCATION])

    r = [(c * normal[0]) - light[LOCATION][0],
         (c * normal[1]) - light[LOCATION][1],
         (c * normal[2]) - light[LOCATION][2]]

    cAlpha = dot_product(r, view) ** SPECULAR_EXP

    return limit_color([light[COLOR][i] * sreflect[i] * cAlpha for i in range(3)])


def limit_color(color):
    return [int(max(min(value, 255), 0)) for value in color]

# vector functions
# normalize vetor, should modify the parameter


def normalize(vector):
    magnitude = math.sqrt(vector[0] * vector[0] +
                          vector[1] * vector[1] +
                          vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude

# Return the dot porduct of a . b


def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

# Calculate the surface normal for the triangle whose first
# point is located at index i in polygons


def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
