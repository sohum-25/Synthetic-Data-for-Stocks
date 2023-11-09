file_path = r'C:\Users\Sohum\Desktop\Synthetic Data for Stocks\symbolz.txt'

# Initialize an empty list to store the data
Symbolz = []

# Read the text file and populate the 'Symbolz' list
with open(file_path, 'r') as file:
    for line in file:
        # Remove any leading or trailing whitespace (e.g., newline characters)
        symbol = line.strip()
        Symbolz.append(symbol)

# Now, 'Symbolz' contains the data from the text file as a list
print(Symbolz)
