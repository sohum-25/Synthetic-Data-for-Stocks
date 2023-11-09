file_path = r'C:\Users\Sohum\Desktop\Synthetic Data for Stocks\token.txt'

# Read the 'tk' value from the file
with open(file_path, 'r') as file:
    tk = file.read().strip()  # Use strip() to remove any leading or trailing white spaces

# Now, 'tk' contains the token read from the file
print("Read token 'tk':", tk)