"""
Export Geomap for PowerPoint Embedding
Creates a standalone HTML file of the UMKM distribution map
"""

import json
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pathlib import Path

def create_standalone_geomap(data_path='data_output/umkm_data.json', output_path='geomap_for_powerpoint.html'):
    """Create standalone geomap HTML file for PowerPoint embedding"""
    
    # Load data
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    df_kecamatan = pd.DataFrame(data['ringkasan_kecamatan'])
    
    # Load district coordinates
    try:
        with open('umkm_tangerang_selatan_analysis/data/tangsel_districts.geojson', 'r') as f:
            districts_data = json.load(f)
    except:
        # Fallback coordinates
        districts_data = {
            "features": [
                {"properties": {"name": "Serpong"}, "geometry": {"coordinates": [106.6647, -6.3197]}},
                {"properties": {"name": "Serpong Utara"}, "geometry": {"coordinates": [106.6747, -6.2997]}},
                {"properties": {"name": "Ciputat"}, "geometry": {"coordinates": [106.7147, -6.3297]}},
                {"properties": {"name": "Ciputat Timur"}, "geometry": {"coordinates": [106.7447, -6.3197]}},
                {"properties": {"name": "Pamulang"}, "geometry": {"coordinates": [106.7347, -6.3497]}},
                {"properties": {"name": "Pondok Aren"}, "geometry": {"coordinates": [106.7147, -6.2797]}},
                {"properties": {"name": "Setu"}, "geometry": {"coordinates": [106.6847, -6.3397]}}
            ]
        }
    
    # Create map figure
    fig = go.Figure()
    
    # Add district markers
    for district in districts_data['features']:
        district_name = district['properties']['name']
        lon, lat = district['geometry']['coordinates']
        
        # Get UMKM data for this district
        district_data = df_kecamatan[df_kecamatan['Kecamatan'] == district_name]
        if not district_data.empty:
            district_data = district_data.iloc[0]
            
            # Calculate marker size and color
            marker_size = max(20, min(60, np.sqrt(district_data['Total']) * 2.5))
            color_intensity = district_data['Total'] / df_kecamatan['Total'].max()
            color = f'rgba(255, {int(255 * (1 - color_intensity))}, 0, 0.9)'
            
            # Add marker
            fig.add_trace(go.Scattermapbox(
                lon=[lon],
                lat=[lat],
                mode='markers',
                marker=dict(
                    size=marker_size,
                    color=color,
                    opacity=0.9,
                    sizemode='diameter'
                ),
                text=f"<b>{district_name}</b><br>" +
                     f"Total UMKM: {district_data['Total']:,}<br>" +
                     f"Mikro: {district_data['Mikro']:,}<br>" +
                     f"Kecil: {district_data['Kecil']:,}",
                name=district_name,
                hoverinfo='text',
                showlegend=False
            ))
    
    # Update layout for PowerPoint embedding
    fig.update_layout(
        mapbox=dict(
            style='open-street-map',
            center=dict(lon=106.7047, lat=-6.3097),
            zoom=11
        ),
        title={
            'text': "Peta Distribusi UMKM Tangerang Selatan",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': 'darkblue'}
        },
        showlegend=False,
        margin=dict(l=10, r=10, t=80, b=10),
        height=600,
        width=900,
        font=dict(family="Arial, sans-serif", size=12),
        annotations=[
            dict(
                text="Ukuran dan warna marker menunjukkan jumlah UMKM per kecamatan",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.5, y=-0.05, xanchor='center', yanchor='top',
                font=dict(size=12, color="gray")
            )
        ]
    )
    
    # Export as HTML
    fig.write_html(
        output_path,
        config={
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],
            'toImageButtonOptions': {
                'format': 'png',
                'filename': 'umkm_map_tangsel',
                'height': 600,
                'width': 900,
                'scale': 2
            }
        },
        include_plotlyjs='cdn'
    )
    
    print(f"✅ Geomap exported successfully to: {output_path}")
    print("📋 To embed in PowerPoint:")
    print("   1. Insert > Web Add-ins > Search for 'Web Viewer'")
    print("   2. Or use Insert > Online Video > paste the HTML file path")
    print("   3. Or take a screenshot of the map for static embedding")

if __name__ == "__main__":
    create_standalone_geomap()
