import load_data
import geo_data
import map
import filter

from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt

def run_all():
        
    DATACOLS = ['beftotalt', 'kvinna', 'man', 'ald0_5', 'ald5_10',
       'ald10_15', 'ald15_20', 'ald20_25', 'ald25_30', 'ald30_35', 'ald35_40',
       'ald40_45', 'ald45_50', 'ald50_55', 'ald55_60', 'ald60_65', 'ald65_70',
       'ald70_75', 'ald75_80', 'ald80_85', 'ald85_90', 'ald90_95', 'ald95_100',
       'ald100w']
    
    
    # Load data
    df = load_data.load()
    print('Data loaded')
    
    # Convert into GeometricDataFrame
    gdf = geo_data.geo(df)
    print('Formatted to GeometricDataFrame')
    
    # Create map plot over population density
    map.plot_map(gdf, 'beftotalt', log=True)
    print('Population map created')
    
    # Filter data and create filter plot
    filtered = filter.apply_filter(gdf)
    print('Data filtered')
    
    # Indicator showing if data survived filtering
    ind = filtered.groupby('block_id')['block_id'].nunique().rename('ind').reset_index() 
    
    # Append indicator to data
    gdf_new = gdf.merge(ind, how='outer', on='block_id').fillna(0)
    
    # Define colormap: light blue for 0, red for 1
    colors = ["#ADD8E6", "#CB4154"]  # light blue to orange
    cmap = LinearSegmentedColormap.from_list("custom_cmap", colors)
    
    # Create map showing where candidate locations are located
    map.plot_map(gdf_new, 'ind', log=False, cmap=cmap, highlight=True)
    print('Indicator map created')
    
    # Plot the allocation of candidates over municipalities 
    mun_counts = filtered.groupby('kommunnamn')['block_id'].apply(lambda x : x.count() // 10)
    mun_counts['Other'] = len(mun_counts[mun_counts == 1])
    mun_counts = mun_counts[mun_counts > 1]
    ax = mun_counts.sort_values().plot.bar()
    print('Municipality plot created')
    output_file = f'../output/candidates_over_muns.png' 
    plt.savefig(output_file, bbox_inches='tight', dpi=300) 
    
    
    # Make interpolation
    filtered['interp'] = filtered['k'] * filtered['year'] + filtered['m']
    filtered['plats'] = filtered['regsonamn'] + ', ' + filtered['kommunnamn']

    # Sort based on growth-rate
    curr = filtered.sort_values(['k', 'block_id', 'year'], ascending=False).groupby('block_id').apply('first')[['plats', 'k', 'young', 'mid', 'old']]#.plot.bar(stacked=True)
    top = curr.nlargest(n=5, columns='k').reset_index()
    
    # Plot allocation data
    ax = top[['young', 'mid', 'old']].plot.bar(stacked=True)
    legend_labels = [f"{i}: {top.loc[i, 'plats']}" for i in range(len(top))]
    mapping_text = "\n".join(legend_labels)
    props = dict(boxstyle='round', facecolor='white', alpha=0.8)
    ax.text(1.05, 0.5, mapping_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='center', bbox=props)
    output_file = f'../output/allocation.png' 
    plt.savefig(output_file, bbox_inches='tight', dpi=300) 

    # create time-series for top 5 candidate areas
    ts = filtered.sort_values(by=['k', 'block_id', 'year'], ascending=False).iloc[:50][['block_id', 'plats', 'year', 'beftotalt', 'interp']]


    # Plot evolution over time and linear interpolation
    plt.figure(figsize=(10,6))
    sns.lineplot(data=ts, x='year', y='beftotalt', hue='plats', marker='o', units='block_id',estimator=None,)
    sns.lineplot(data=ts, x='year', y='interp', hue='plats', marker='o', alpha=0.5, legend=False, units='block_id',estimator=None,)
    plt.legend(title='kommunnamn', bbox_to_anchor=(1.05, 1), loc='upper left')
    output_file = f'../output/forecast.png' 
    plt.ylabel("Population")
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.savefig(output_file, bbox_inches='tight', dpi=300) 
    
if __name__ == '__main__':
    run_all()