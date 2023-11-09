from historic_data import UpdateHistoricData
csv_path = 'ind_nifty100list (1).csv'
Symbolz = UpdateHistoricData(csv_path)

# Specify the file path
file_path = r'C:\Users\Sohum\Desktop\Synthetic Data for Stocks\symbolz.txt'

# Save the 'Symbolz' list as a text file
with open(file_path, 'w') as file:
    for symbol in Symbolz:
        file.write(symbol + '\n')

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