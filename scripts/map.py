import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
def plot_map(gdf : gpd.GeoDataFrame, column : str, log : bool, cmap : str = 'YlOrRd', highlight : bool = False):
    
    gdf_new = gdf.dissolve(by=['block_id'], aggfunc='last')
    
    if log:
        gdf_new[f'log_{column}'] = np.log1p(gdf_new[column] - gdf_new[column].min())
        column = f'log_{column}'

    fig, ax = plt.subplots(figsize=(4,8))

    gdf_new.plot(
        column=column,
        cmap=cmap,
        ax=ax,
        legend=False

    )
    
    if highlight:
        highlights = gdf_new[gdf_new[column] > gdf_new[column].quantile(q=0.5)]
        
        highlights['geometry'] = highlights.centroid

        # Plot circles on top
        highlights.plot(
            ax=ax,
            color='#CB4154',
            markersize=10,
            alpha=0.4,
            marker='o'
        )

    ax.set_axis_off()
    output_file = f'../output/{column}_map.png' 
    plt.savefig(output_file, bbox_inches='tight', dpi=300) 

    plt.close(fig)
    