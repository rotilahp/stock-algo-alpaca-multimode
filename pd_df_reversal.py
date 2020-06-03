import pandas as pd

def reversePandasDf(df,_column):
    df_rev = pd.DataFrame()
    for i, value in enumerate(df.iloc[::-1]):
        df_rev = df_rev.append({_column:float(value)},ignore_index=True)
    return df_rev

def reversePandasDf_string(df,_column):
    df_rev = pd.DataFrame(columns=[_column])
    for i, value in enumerate(df.iloc[::-1]):
        df_rev = df_rev.append({_column:value},ignore_index=True)
    return df_rev
