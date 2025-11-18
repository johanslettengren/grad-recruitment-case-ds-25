import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt

def apply_filter(gdf : gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    
    """ Filter based on the follwoing questions:
    
    Is the population at least 5000?
    Is the growth positive?
    Is the population aging?
    Is there an influx of young families?
    
 """
    
    # Create relevant columns
    gdf['pct_change'] = gdf.groupby('block_id')['beftotalt'].pct_change() * 100
    gdf['diff'] = gdf['beftotalt'].diff()
    gdf['child'] = sum(gdf[f'ald{y}_{y+5}'] for y in range(0, 15, 5))
    gdf['young'] = sum(gdf[f'ald{y}_{y+5}'] for y in range(0, 20, 5))
    gdf['mid'] = sum(gdf[f'ald{y}_{y+5}'] for y in range(20, 65, 5))
    gdf['premium'] = sum(gdf[f'ald{y}_{y+5}'] for y in range(25, 45, 5))
    gdf['old'] = sum(gdf[f'ald{y}_{y+5}'] for y in range(65, 100, 5)) + gdf[f'ald100w']
    
    
    total_block = gdf['block_id'].nunique()
    
    # Look at current population
    gdf['curr_pop'] = gdf.groupby('block_id')['beftotalt'].transform('first')
    
    
    # Filter types
    filter_types = ['dense', 'growing', 'non-aging', 'family-influx', 'all']

    # How percent of old people increases/decreases
    gdf['pct_old'] = gdf['old'] / gdf['beftotalt']
    gdf['pct_old_k'] = gdf.groupby('block_id')['year'].transform(lambda t: np.polyfit(t, gdf.loc[t.index, 'pct_old'], 1)[0])
    
    # How number of children grows/declines (proxy for family influx)
    gdf['pct_child'] = gdf['child'] / gdf['beftotalt']
    gdf['pct_child_k'] = gdf.groupby('block_id')['year'].transform(lambda t: np.polyfit(t, gdf.loc[t.index, 'pct_child'], 1)[0])
    
    
    nums = []
    nums.append(gdf[gdf['curr_pop'] >= 5000]['block_id'].nunique() / total_block)
    nums.append(gdf[gdf['k'] > 0]['block_id'].nunique() / total_block)
    nums.append(gdf[gdf['pct_old_k'] <= 0]['block_id'].nunique() / total_block)
    nums.append(gdf[gdf['pct_child_k'] > 0]['block_id'].nunique() / total_block)
    

    gdf_new = gdf[(gdf['curr_pop'] >= 5000) & (gdf['k'] > 0) & (gdf['pct_old_k'] <= 0) & (gdf['pct_child_k'] > 0)]
    
    nums.append(gdf_new['block_id'].nunique() / total_block)
    
    
    # Plot and save
    fig, ax = plt.subplots(figsize=(8,8))
    ax.bar(x=filter_types, height=nums)
    output_file = '../output/filter_stages.png'  # can be .png, .pdf, etc.
    plt.savefig(output_file, bbox_inches='tight', dpi=300)  # tight bbox removes extra whitespace
    plt.close(fig)
    
    return gdf_new