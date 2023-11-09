from historic_data import UpdateHistoricData
csv_path = 'ind_nifty100list (1).csv'
Symbolz = UpdateHistoricData(csv_path)

# Specify the file path
file_path = r'C:\Users\Sohum\Desktop\Synthetic Data for Stocks\symbolz.txt'

# Save the 'Symbolz' list as a text file
with open(file_path, 'w') as file:
    for symbol in Symbolz:
        file.write(symbol + '\n')