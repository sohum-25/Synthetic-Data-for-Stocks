import pandas as pd
from statsmodels.tsa.stattools import coint
import yfinance as yf
import pandas as pd
import pandas as pd

def FillerDataFrames(path):
    Stocks = pd.read_csv(path)
    Stocks['Symbol'] = Stocks['Symbol'].apply(lambda x: x + ".NS" if not x.endswith(".NS") else x)
    correlation = yf.download(tickers=Stocks['Symbol'].to_list(), period='20d', interval='2m')['Close']
    
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
    included_stocks = set()  # To keep track of stocks included in pairs

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

                # Mark the stocks as included in pairs
                included_stocks.add(stock1)
                included_stocks.add(stock2)

            # Mark the pair as checked
            checked_pairs.add(pair)

    # Sort the list based on the ascending order of the last item (p_value) in each sublist
    lst = sorted(lst, key=lambda x: x[2])

    # Select the top values and ensure that no stock appears in more than one pair
    top_pairs = []
    for pair in lst:
        if pair[0] not in included_stocks or pair[1] not in included_stocks:
            top_pairs.append(pair)
            included_stocks.add(pair[0])
            included_stocks.add(pair[1])

    return top_pairs[:10]

def ListCorrection(lst):
    flattened_list = [item for sublist in lst for item in sublist]
    cleaned_list = [item.replace(".NS", "").replace(".NSE:", "").replace("-EQ", "") for item in flattened_list]
    return cleaned_list



