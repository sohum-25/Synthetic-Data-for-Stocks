import sqlite3
import pandas as pd

def CalculateParameters(database_path, symbol_list, i,TotalCapital,fyers,inTrade,activeLongPosition,activeShortPosition):
    TotalCapital=TotalCapital
    inTrade=inTrade
    activeLongPosition=activeLongPosition
    activeShortPosition=activeShortPosition
    conn = sqlite3.connect(database_path)
    
    try:
        # Retrieve the latest 50 records from the database
        query = "SELECT * FROM tick_data ORDER BY Datetime DESC LIMIT 30"
        df = pd.read_sql_query(query, conn)
        
        # Set the 'Datetime' column as the index
        df.set_index('Datetime', inplace=True)
        
        # Select the columns corresponding to the two symbols for analysis
        symbol1 = symbol_list[2 * i]
        symbol2 = symbol_list[2 * i + 1]

        symbol1Socket = "NSE:" + symbol_list[2 * i] + "-EQ"
        symbol2Socket = "NSE:" + symbol_list[2 * i + 1] + "-EQ"
        df = df[[symbol1, symbol2]]
        
        # Calculate the ratio between the two symbols
        df['Ratio'] = df[symbol1] / df[symbol2]
        
        # Calculate the EMA (Exponential Moving Average) of the ratio with a window of 20
        df['EMA'] = df['Ratio'].rolling(20).mean()
        
        # Calculate the upper and lower standard deviation bands
        df['StdDown'] = df['EMA'] - df['EMA'].rolling(20).std()
        df['StdUp'] = df['EMA'] + df['EMA'].rolling(20).std()
        
        # Initialize trade-related variables
        inTrade = 0
        activeLongPosition = 0
        activeShortPosition = 0
        
        symbol1Qty=int((TotalCapital/2)/df[symbol1].iloc[-1])
        symbol2Qty=int((TotalCapital/2)/df[symbol2].iloc[-1])


        LongSide = [
    {
    "symbol": symbol1Socket,
    "qty":symbol1Qty,
    "type":2,
    "side":1,
    "productType":"INTRADAY",
    "limitPrice":0,
    "stopPrice":0,
    "validity":"DAY",
    "disclosedQty":0,
    "offlineOrder":False,
},
{
    "symbol": symbol2Socket,
    "qty":symbol2Qty,
    "type":2,
    "side":-1,
    "productType":"INTRADAY",
    "limitPrice":0,
    "stopPrice":0,
    "validity":"DAY",
    "disclosedQty":0,
    "offlineOrder":False,
}]
        ShortSide = [
    {
    "symbol": symbol1Socket,
    "qty":symbol1Qty,
    "type":2,
    "side":-1,
    "productType":"INTRADAY",
    "limitPrice":0,
    "stopPrice":0,
    "validity":"DAY",
    "disclosedQty":0,
    "offlineOrder":False,
},
{
    "symbol": symbol2Socket,
    "qty":symbol2Qty,
    "type":2,
    "side":1,
    "productType":"INTRADAY",
    "limitPrice":0,
    "stopPrice":0,
    "validity":"DAY",
    "disclosedQty":0,
    "offlineOrder":False,
}]


        # Check trading conditions
        if df['Ratio'].iloc[-1] < df['StdDown'].iloc[-1] and not inTrade:
           
            fyers.place_basket_orders(data=LongSide)
            inTrade = True
            activeLongPosition = 1
        
        if df['Ratio'].iloc[-1] > df['StdUp'].iloc[-1] and not inTrade:
            # Enter a Short Position
            fyers.place_basket_orders(data=ShortSide)
            inTrade = True
            activeShortPosition = 1
        
        # Check for closing positions
        if inTrade:
            if activeLongPosition and df['Ratio'].iloc[-1] >= df['EMA'].iloc[-1]:
                # Close the Long Position
                fyers.exit_positions(data={})
                response=fyers.positions()
                TotalCapital+=response["overall"]["pl_realized"]
                inTrade = False
                activeLongPosition = 0
            if activeShortPosition and df['Ratio'].iloc[-1] <= df['EMA'].iloc[-1]:
                # Close the Short Position
                fyers.exit_positions(data={})
                response=fyers.positions()
                TotalCapital+=response["overall"]["pl_realized"]
                inTrade = False
                activeShortPosition = 0

    except Exception as e:
        print(f"Error analyzing tick data: {e}")
        return None
    finally:
        conn.close()





