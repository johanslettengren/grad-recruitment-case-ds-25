import pandas as pd

def load()->pd.DataFrame:
    """merge data from 2015-2024 plus link data"""
    
    # Columns with demographic data 
    DATACOLS = ['beftotalt', 'kvinna', 'man', 'ald0_5', 'ald5_10',
       'ald10_15', 'ald15_20', 'ald20_25', 'ald25_30', 'ald30_35', 'ald35_40',
       'ald40_45', 'ald45_50', 'ald50_55', 'ald55_60', 'ald60_65', 'ald65_70',
       'ald70_75', 'ald75_80', 'ald80_85', 'ald85_90', 'ald90_95', 'ald95_100',
       'ald100w']
    
    
    
    years = [y for y in range(2015, 2025)] # 2015 - 2024
    files = [f"../data/geoparquet/befolkning_1km_{y}.parquet" for y in years] # file paths for population files
    df = pd.concat(( pd.read_parquet(file, engine='fastparquet') for file in files), ignore_index=True) # concat all dataframes
    df['year'] = df['referenstid'].apply(lambda x : x[0:4]).astype(int) # extract year
    df = df.drop(['objectid', 'rutid_scb', 'rutstorl', 'referenstid', 'geometry'], axis=1) # drop unused columns
    
    # Find the squares with incomplete data
    ids = df.groupby('rutid_inspire')['beftotalt'].apply(len)
    ids = ids[ids != 10].index
    
    # For this subset we add the missing years
    idx = pd.MultiIndex.from_product([ids, years], names=['rutid_inspire', 'year']).to_frame(index=False)
    df = df.merge(idx, how='outer', on=['rutid_inspire', 'year'], validate='many_to_many')

    # Number of missing values before filling
    num_missing_pre = len(ids)
    print('# IDs with missing years', num_missing_pre)
    
    # backward fill then forward fill
    for c in DATACOLS:
        df[c] = df.groupby('rutid_inspire')[c].ffill().bfill()
        
    
    df_link = pd.read_parquet("../data/geoparquet/RegSO_2025_Link.parquet", engine="fastparquet") # read link data
    df = df.merge(df_link, on="rutid_inspire", how="inner", validate="many_to_many") # merge link data
    
    # Check that there is no missing values
    num_missing_post = df.isna().sum().sum()
    print('# NaNs in final df', num_missing_post)
    
    return df