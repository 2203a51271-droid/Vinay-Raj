import math

def calculate_area(shape, x, y=0):
    if shape == "rectangle":
        return x * y
    elif shape == "square":
        return x * x
    elif shape == "circle":
        return math.pi * x * x
    else:
        return "Invalid shape"

# Function calls with outputs
print("Rectangle area (10 x 5):", calculate_area("rectangle", 10, 5))
print("Square area (side=4):", calculate_area("square", 4))
print("Circle area (radius=7):", calculate_area("circle", 7))
print("Invalid example:", calculate_area("triangle", 6, 3))
