import pandas as pd
import geopandas as gpd
import numpy as np
from shapely import wkb

def geo(df : pd.DataFrame)->gpd.GeoDataFrame:
    
    DATACOLS = ['beftotalt', 'kvinna', 'man', 'ald0_5', 'ald5_10',
       'ald10_15', 'ald15_20', 'ald20_25', 'ald25_30', 'ald30_35', 'ald35_40',
       'ald40_45', 'ald45_50', 'ald50_55', 'ald55_60', 'ald60_65', 'ald65_70',
       'ald70_75', 'ald75_80', 'ald80_85', 'ald85_90', 'ald90_95', 'ald95_100',
       'ald100w']
    
    df['geometry'] = df['geometry'].apply(wkb.loads) # format geometry
    gdf = gpd.GeoDataFrame(df, geometry='geometry', crs="EPSG:4326") # turn into GeoDataFrame
    
    gdf = gdf.to_crs(epsg=3857) # Make sure CRS is in meters (not degrees)

    gdf['x'] = gdf.centroid.x       # Get centroid coordinates
    gdf['y'] = gdf.centroid.y       # Get centroid coordinates

    block_size = 5000  # 5 km in meters

    # Compute block IDs by integer division
    gdf['block_x'] = (gdf['x'] // block_size).astype(int)
    gdf['block_y'] = (gdf['y'] // block_size).astype(int)

    # Create a combined block ID
    gdf['block_id'] = gdf['block_x'].astype(str) + "_" + gdf['block_y'].astype(str)
    
    mode = lambda x: x.mode()[0]
    
    # Dissolve to aggregate into 5 km^2 blocks
    aggdict = {'kommunnamn' : mode, 'regsonamn' : mode}
    aggdict.update({col: 'sum' for col in DATACOLS})
    gdf_5km = gdf.dissolve(by=['block_id', 'year'], aggfunc=aggdict)
    gdf_5km = gdf_5km.reset_index()

    # Make a linear interpolation
    coeffs = gdf_5km.groupby('block_id')['year'].apply(lambda t: np.polyfit(t, gdf_5km.loc[t.index, 'beftotalt'], 1)).rename('coeffs')
    gdf_5km = gdf_5km.merge(coeffs, on='block_id')

    # k is slope and m is intercent
    gdf_5km['k'] = gdf_5km['coeffs'].apply(lambda x : x[0])
    gdf_5km['m'] = gdf_5km['coeffs'].apply(lambda x : x[1])
    
    # sort and return
    return gdf_5km.sort_values(by=['block_id', 'year'], ascending=False)