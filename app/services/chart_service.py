import pandas as pd 

def create_dataframe(ohlcv):

    df = pd.DataFrame(ohlcv,columns=["time","open","high","low","close","volume"])

    df["time"] = pd.to_datetime(df["time"] , unit = "s")
    
    return df