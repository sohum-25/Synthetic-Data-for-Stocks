import pandas as pd
from statsmodels.tsa.stattools import coint
import yfinance as yf

def find_relevant_pairs(data_path, threshold=0.05):
    Stocks = pd.read_csv(data_path)
    Stocks['Symbol'] = Stocks['Symbol'].apply(lambda x: x + ".NS" if not x.endswith(".NS") else x)
    correlation = yf.download(tickers=Stocks['Symbol'].to_list(), period='3d', interval='2m')['Close']
    correlation = correlation.dropna()
    Stocks = Stocks[Stocks['Symbol'].isin(correlation.columns)]
    Stocks = Stocks.reset_index()
    stock_list = Stocks['Symbol'].to_list()

    Valid_pairs = []
    for i in range(len(Stocks)):
        for j in range(len(Stocks)):
            if (Stocks['Industry'][i] == Stocks['Industry'][j]) and (Stocks['Symbol'][i] != Stocks['Symbol'][j]):
                Valid_pairs.append((Stocks['Symbol'][i], Stocks['Symbol'][j]))

    ValidPairs = pd.DataFrame(Valid_pairs, columns=['Stock1', 'Stock2'])

    def get_relevant_pairs(look_back_data, threshold, valid_pairs):
        lst = []
        checked_pairs = set()  # To keep track of checked pairs
        first_values_set = set()  # To keep track of unique first values

        for i in range(len(valid_pairs)):
            stock1 = valid_pairs['Stock1'][i]
            stock2 = valid_pairs['Stock2'][i]

            # Ensure that stock1 and stock2 are in the same order (a, b)
            pair = (stock1, stock2) if stock1 < stock2 else (stock2, stock1)

            # Check if the pair has already been processed
            if pair not in checked_pairs:
                stock1_data = look_back_data[stock1]
                stock2_data = look_back_data[stock2]

                p_value = coint(stock1_data, stock2_data)[1]
                corr_value = stock1_data.corr(stock2_data)

                if p_value <= threshold and corr_value > 0:
                    lst.append([stock1, stock2])

                # Mark the pair as checked
                checked_pairs.add(pair)

                # Track the first value in the pair
                first_values_set.add(pair[0])

        return lst

    relevant_pairs = get_relevant_pairs(correlation, threshold, ValidPairs)

    return relevant_pairs[:10]

data_path = 'ind_nifty100list (1).csv'
threshold = 0.05
result = find_relevant_pairs(data_path, threshold)
print(result)
