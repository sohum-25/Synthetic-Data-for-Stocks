import pandas as pd
from statsmodels.tsa.stattools import coint
import yfinance as yf
import pandas as pd
import pandas as pd

def FillerDataFrames(path):
    Stocks = pd.read_csv(path)
    Stocks['Symbol'] = Stocks['Symbol'].apply(lambda x: x + ".NS" if not x.endswith(".NS") else x)
    correlation = yf.download(tickers=Stocks['Symbol'].to_list(), period='3d', interval='2m')['Close']
    correlation = correlation.dropna()
    correlation = correlation.dropna(axis=1)
    Stocks = Stocks[Stocks['Symbol'].isin(correlation.columns)]
    Stocks = Stocks.reset_index()
    Valid_pairs = []

    for i in range(len(Stocks)):
        for j in range(len(Stocks)):
            if (Stocks['Industry'][i] == Stocks['Industry'][j]) and (Stocks['Symbol'][i] != Stocks['Symbol'][j]):
                Valid_pairs.append((Stocks['Symbol'][i], Stocks['Symbol'][j], Stocks['Industry'][i], Stocks['Industry'][j]))

    ValidPairs = pd.DataFrame(Valid_pairs, columns=['Stock1', 'Stock2', 'Industry1', 'Industry2'])
    return ValidPairs,correlation


def GetRelevantPairs(Look_back_DataFrame, threshold, ValidPairs):
    lst = []
    checked_pairs = set()  # To keep track of checked pairs
    first_values_set = set()  # To keep track of unique first values

    for i in range(len(ValidPairs)):
        stock1 = ValidPairs['Stock1'][i]
        stock2 = ValidPairs['Stock2'][i]

        # Ensure that stock1 and stock2 are in the same order (a, b)
        pair = (stock1, stock2) if stock1 < stock2 else (stock2, stock1)

        # Check if the pair has already been processed
        if pair not in checked_pairs:
            stock1_data = Look_back_DataFrame[stock1]
            stock2_data = Look_back_DataFrame[stock2]
            
            p_value = coint(stock1_data, stock2_data)[1]
            corr_value = stock1_data.corr(stock2_data)

            if p_value <= threshold and corr_value > 0:
                lst.append((stock1, stock2, p_value))

            # Mark the pair as checked
            checked_pairs.add(pair)

            # Track the first value in the pair
            first_values_set.add(pair[0])

    # Sort the list based on the ascending order of the last item (p_value) in each sublist
    lst = sorted(lst, key=lambda x: x[2])

    # Drop duplicates based on the first value
    unique_pairs = []
    for pair in lst:
        if pair[0] in first_values_set:
            unique_pairs.append(pair)
            first_values_set.remove(pair[0])  # Remove the first value to avoid duplicates

    # Select the top values
    top_5_pairs = unique_pairs
    top_5_pairs = [[sublist[0], sublist[1]] for sublist in top_5_pairs]

    return top_5_pairs[:10]

def ListCorrection(lst):
    flattened_list = [item for sublist in lst for item in sublist]
    cleaned_list = [item.replace(".NS", "").replace(".NSE:", "").replace("-EQ", "") for item in flattened_list]
    return cleaned_list



