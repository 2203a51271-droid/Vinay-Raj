import math

def rectangle_area(x, y):
    return x * y
def square_area(x):
    return x * x
def circle_area(x):
    return math.pi * x * x

area_functions = {
    "rectangle": rectangle_area,
    "square": square_area,
    "circle": circle_area
}
def calculate_area(shape, x, y=0):
    if shape not in area_functions:
        raise ValueError(f"Unsupported shape: {shape}")
    
    if shape == "rectangle":
        return area_functions[shape](x, y)
    else:
        return area_functions[shape](x)
print(calculate_area("rectangle", 5, 10))  
print(calculate_area("square", 7))         
print(calculate_area("circle", 3))