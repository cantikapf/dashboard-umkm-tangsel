"""
📈 UMKM Dashboard - Interactive Web Dashboard
Visualizes UMKM data with interactive charts and maps
"""

import json
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from pathlib import Path

class UMKMDashboard:
    def __init__(self, data_path='data_output/umkm_data.json'):
        """Initialize dashboard with data"""
        self.data_path = Path(data_path)
        self.load_data()
        
        # Initialize Dash app
        self.app = Dash(__name__, 
                       external_stylesheets=[dbc.themes.BOOTSTRAP],
                       title='Dashboard UMKM Tangsel')
        
        self.setup_layout()
        self.setup_callbacks()
    
    def load_data(self):
        """Load data from JSON file"""
        with open(self.data_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
            
        # Convert to DataFrames for easier manipulation
        self.df = pd.DataFrame(self.data['data_lengkap'])
        self.df_kecamatan = pd.DataFrame(self.data['ringkasan_kecamatan'])
        self.df_bidang = pd.DataFrame(self.data['ringkasan_bidang'])
        
    def create_overview_cards(self):
        """Create overview statistics cards"""
        stats = self.data['statistik']
        
        cards = [
            dbc.Card([
                dbc.CardBody([
                    html.H4("Total UMKM", className="card-title"),
                    html.H2(f"{stats['total_umkm']:,}", className="card-text text-primary")
                ])
            ], className="mb-4"),
            
            dbc.Card([
                dbc.CardBody([
                    html.H4("UMKM Mikro", className="card-title"),
                    html.H2(f"{stats['total_mikro']:,}", className="card-text text-success")
                ])
            ], className="mb-4"),
            
            dbc.Card([
                dbc.CardBody([
                    html.H4("UMKM Kecil", className="card-title"),
                    html.H2(f"{stats['total_kecil']:,}", className="card-text text-info")
                ])
            ], className="mb-4")
        ]
        
        return dbc.Row([dbc.Col(card, width=4) for card in cards])
    
    
    def create_geomap(self):
        """Create geographic distribution map with colored districts"""
        # Load district boundaries from GeoJSON
        try:
            with open('umkm_tangerang_selatan_analysis/data/tangsel_districts.geojson', 'r') as f:
                districts_data = json.load(f)
        except:
            # Fallback to hardcoded coordinates if file not found
            districts_data = {
                "features": [
                    {"properties": {"name": "Serpong", "center": [106.6647, -6.3197]}, "geometry": {"type": "Polygon", "coordinates": [[[106.64, -6.34], [106.69, -6.34], [106.69, -6.29], [106.64, -6.29], [106.64, -6.34]]]}},
                    {"properties": {"name": "Serpong Utara", "center": [106.6747, -6.2997]}, "geometry": {"type": "Polygon", "coordinates": [[[106.65, -6.32], [106.70, -6.32], [106.70, -6.27], [106.65, -6.27], [106.65, -6.32]]]}},
                    {"properties": {"name": "Ciputat", "center": [106.7147, -6.3297]}, "geometry": {"type": "Polygon", "coordinates": [[[106.69, -6.35], [106.74, -6.35], [106.74, -6.30], [106.69, -6.30], [106.69, -6.35]]]}},
                    {"properties": {"name": "Ciputat Timur", "center": [106.7447, -6.3197]}, "geometry": {"type": "Polygon", "coordinates": [[[106.72, -6.34], [106.77, -6.34], [106.77, -6.29], [106.72, -6.29], [106.72, -6.34]]]}},
                    {"properties": {"name": "Pamulang", "center": [106.7347, -6.3497]}, "geometry": {"type": "Polygon", "coordinates": [[[106.71, -6.37], [106.76, -6.37], [106.76, -6.32], [106.71, -6.32], [106.71, -6.37]]]}},
                    {"properties": {"name": "Pondok Aren", "center": [106.7147, -6.2797]}, "geometry": {"type": "Polygon", "coordinates": [[[106.69, -6.30], [106.74, -6.30], [106.74, -6.25], [106.69, -6.25], [106.69, -6.30]]]}},
                    {"properties": {"name": "Setu", "center": [106.6847, -6.3397]}, "geometry": {"type": "Polygon", "coordinates": [[[106.66, -6.36], [106.71, -6.36], [106.71, -6.31], [106.66, -6.31], [106.66, -6.36]]]}}
                ]
            }
        
        # Create choropleth map using mapbox
        try:
            # Prepare data for choropleth
            district_names = []
            district_values = []
            
            for district in districts_data['features']:
                district_name = district['properties']['name']
                district_data = self.df_kecamatan[self.df_kecamatan['Kecamatan'] == district_name]
                
                if not district_data.empty:
                    district_names.append(district_name)
                    district_values.append(district_data.iloc[0]['Total'])
            
            # Create choropleth mapbox
            fig = px.choropleth_mapbox(
                geojson=districts_data,
                locations=district_names,
                color=district_values,
                color_continuous_scale="Viridis",
                range_color=(0, max(district_values)),
                mapbox_style="open-street-map",
                zoom=10,
                center={"lat": -6.3097, "lon": 106.7047},
                opacity=0.7,
                labels={'color': 'Jumlah UMKM'},
                title="Peta Distribusi UMKM Tangerang Selatan"
            )
            
            # Add markers for each district
            for district in districts_data['features']:
                district_name = district['properties']['name']
                district_data = self.df_kecamatan[self.df_kecamatan['Kecamatan'] == district_name]
                
                if not district_data.empty:
                    district_data = district_data.iloc[0]
                    center_coords = district['properties']['center']
                    
                    fig.add_trace(go.Scattermapbox(
                        lat=[center_coords[1]],
                        lon=[center_coords[0]],
                        mode='markers+text',
                        marker=dict(
                            size=max(15, min(40, district_data['Total'] / 500)),
                            color='white',
                            opacity=0.9
                        ),
                        text=str(district_data['Total']),
                        textfont=dict(size=12, color='black'),
                        textposition='middle center',
                        hovertext=f"<b>{district_name}</b><br>" +
                                 f"Total UMKM: {district_data['Total']:,}<br>" +
                                 f"Mikro: {district_data['Mikro']:,}<br>" +
                                 f"Kecil: {district_data['Kecil']:,}",
                        hoverinfo='text',
                        name=district_name,
                        showlegend=False
                    ))
            
            fig.update_layout(
                mapbox_style="open-street-map",
                height=600,
                margin=dict(l=0, r=0, t=60, b=0)
            )
            
        except Exception as e:
            # Fallback to scatter geo if choropleth fails
            fig = go.Figure()
            
            # Define color palette for districts
            color_palette = [
                '#FF6B6B',  # Red
                '#4ECDC4',  # Teal
                '#45B7D1',  # Blue
                '#96CEB4',  # Green
                '#FFEAA7',  # Yellow
                '#DDA0DD',  # Plum
                '#98D8C8'   # Mint
            ]
            
            for i, district in enumerate(districts_data['features']):
                district_name = district['properties']['name']
                district_data = self.df_kecamatan[self.df_kecamatan['Kecamatan'] == district_name]
                
                if not district_data.empty:
                    district_data = district_data.iloc[0]
                    base_color = color_palette[i % len(color_palette)]
                    
                    # Convert hex to RGB
                    hex_color = base_color.lstrip('#')
                    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
                    
                    # Add polygon for district boundary
                    if district['geometry']['type'] == 'Polygon':
                        coords = district['geometry']['coordinates'][0]
                        lons = [coord[0] for coord in coords]
                        lats = [coord[1] for coord in coords]
                        
                        fig.add_trace(go.Scattergeo(
                            lon=lons,
                            lat=lats,
                            mode='lines',
                            fill='toself',
                            fillcolor=f'rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 0.3)',
                            line=dict(color='white', width=2),
                            name=district_name,
                            hoverinfo='skip',
                            showlegend=False
                        ))

                    # Add center marker with UMKM count
                    center_coords = district['properties']['center']
                    marker_size = max(20, min(60, (district_data['Total'] / 1000) * 15))
                    
                    fig.add_trace(go.Scattergeo(
                        lon=[center_coords[0]],
                        lat=[center_coords[1]],
                        mode='markers+text',
                        marker=dict(
                            size=marker_size,
                            color=base_color,
                            opacity=0.8,
                            line=dict(color='white', width=2)
                        ),
                        text=str(district_data['Total']),
                        textfont=dict(size=12, color='white'),
                        textposition='middle center',
                        hovertext=f"<b>{district_name}</b><br>" +
                                 f"Total UMKM: {district_data['Total']:,}<br>" +
                                 f"Mikro: {district_data['Mikro']:,}<br>" +
                                 f"Kecil: {district_data['Kecil']:,}",
                        hoverinfo='text',
                        name=district_name,
                        showlegend=True
                    ))

            # Update layout with map styling
            fig.update_layout(
                geo=dict(
                    projection_type='mercator',
                    showland=True,
                    landcolor='rgb(243, 243, 243)',
                    coastlinecolor='rgb(204, 204, 204)',
                    showcoastlines=True,
                    showocean=True,
                    oceancolor='rgb(230, 245, 255)',
                    showcountries=True,
                    countrycolor='rgb(204, 204, 204)',
                    showsubunits=True,
                    subunitcolor='rgb(217, 217, 217)',
                    center=dict(lon=106.7047, lat=-6.3097),
                    lonaxis=dict(range=[106.62, 106.78]),
                    lataxis=dict(range=[-6.35, -6.25]),
                    bgcolor='rgba(0,0,0,0)',
                    resolution=50
                ),
                title="Peta Distribusi UMKM Tangerang Selatan<br><sub>Lingkaran menunjukkan jumlah UMKM per kecamatan</sub>",
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="top",
                    y=1,
                    xanchor="left",
                    x=1.02
                ),
                margin=dict(l=0, r=150, t=60, b=0),
                height=600
            )
        
        return dcc.Graph(figure=fig)
    
    def setup_layout(self):
        """Set up dashboard layout"""
        self.app.layout = dbc.Container([
            # Header
            html.H1("Dashboard UMKM Tangerang Selatan", 
                   className="text-center my-4"),
            
            # Overview Statistics
            self.create_overview_cards(),
            
            
            # Geomap
            dbc.Row([
                dbc.Col([
                    self.create_geomap()
                ], width=12)
            ]),
            
            # Footer
            html.Footer([
                html.P(f"Last updated: {self.data['metadata']['last_updated']}",
                       className="text-center text-muted mt-4")
            ])
            
        ], fluid=True)
    
    def setup_callbacks(self):
        """Set up interactive callbacks"""
        @self.app.callback(
            Output("export-button", "n_clicks"),
            [Input("export-button", "n_clicks")]
        )
        def export_map(n_clicks):
            if n_clicks is not None and n_clicks > 0:
                self.export_geomap()
            return 0
    
    def run_server(self, debug=True, port=8050):
        """Run the dashboard server"""
        self.app.run_server(debug=debug, port=port)

def main():
    """Main execution function"""
    dashboard = UMKMDashboard()
    dashboard.run_server()

if __name__ == "__main__":
    main()
