def read_file(filename):
    try:
        with open(filename, "r") as f:
            data = f.read()
        return data
    except FileNotFoundError:
        return f"Error: {filename} not found."

# Example usage
print("Reading sample.txt contents:")
print(read_file("sample.txt"))