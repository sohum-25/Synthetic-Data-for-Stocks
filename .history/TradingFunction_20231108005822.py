import sqlite3
import pandas as pd

def CalculateParameters(database_path, symbol_list,i):
    conn = sqlite3.connect(database_path)
    try:
        query = "SELECT * FROM tick_data ORDER BY Datetime DESC LIMIT 50"
        df = pd.read_sql_query(query, conn)
        df.set_index('Datetime', inplace=True)
        df = df[[symbol_list[2*i],symbol_list[2*i+1]]]
        df['Ratio'] = df.iloc[:, 0] / df.iloc[:, 1]
        df['EMA'] = df['Ratio'].rolling(20).mean()
        df['StdDown'] = df['EMA'] - df['EMA'].rolling(20).std()
        df['StdUp'] = df['EMA'] + df['EMA'].rolling(20).std()
        inTrade=False
        activeLongPosition=0
        activeShortPosition=0
        if(df['Ratio'].iloc[-1]<df['StdDown'].iloc[-1] and inTrade==False):
            #Enter Long Position
            inTrade=True
            activeLongPosition=1
        if(df['Ratio'].iloc[-1]>df['StdUp'].iloc[-1] and inTrade==False):
            #Enter Short Position
            inTrade=True
            activeShortPosition=1
        if(inTrade):
            if(activeLongPosition):
                if(df['Ratio'].iloc[-1]>=df['EMA'].iloc[-1]):
                    #Close the Long Position
                    inTrade=False
                    activeLongPosition=0
            if(activeShortPosition):
                if(df['Ratio'].iloc[-1]<=df['EMA'].iloc[-1]):
                    #Close the Short Position
                    inTrade=False
                    activeShortPosition=0
    except Exception as e:
        print(f"Error analyzing tick data: {e}")
        return None
    finally:
        conn.close()

