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
        """Create geographic distribution map"""
        # Load district coordinates from GeoJSON
        try:
            with open('umkm_tangerang_selatan_analysis/data/tangsel_districts.geojson', 'r') as f:
                districts_data = json.load(f)
        except:
            # Fallback to hardcoded coordinates if file not found
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
        
        # Create the map figure
        fig = go.Figure()

        # Add district markers with UMKM data
        for district in districts_data['features']:
            district_name = district['properties']['name']
            lon, lat = district['geometry']['coordinates']
            
            # Get UMKM data for this district
            district_data = self.df_kecamatan[self.df_kecamatan['Kecamatan'] == district_name]
            if not district_data.empty:
                district_data = district_data.iloc[0]
                
                # Calculate marker size based on total UMKM (scale it appropriately)
                marker_size = max(15, min(50, np.sqrt(district_data['Total']) * 2))
                
                # Create color based on UMKM density
                color_intensity = district_data['Total'] / self.df_kecamatan['Total'].max()
                color = f'rgba(255, {int(255 * (1 - color_intensity))}, 0, 0.8)'
                
                # Add marker for this district
                fig.add_trace(go.Scattermapbox(
                    lon=[lon],
                    lat=[lat],
                    mode='markers',
                    marker=dict(
                        size=marker_size,
                        color=color,
                        opacity=0.8
                    ),
                    text=f"<b>{district_name}</b><br>" +
                         f"Total UMKM: {district_data['Total']:,}<br>" +
                         f"Mikro: {district_data['Mikro']:,}<br>" +
                         f"Kecil: {district_data['Kecil']:,}",
                    name=district_name,
                    hoverinfo='text',
                    showlegend=False
                ))

        # Update layout with map styling
        fig.update_layout(
            mapbox=dict(
                style='open-street-map',
                center=dict(lon=106.7047, lat=-6.3097),
                zoom=11
            ),
            title="Peta Distribusi UMKM Tangerang Selatan<br><sub>Ukuran dan warna marker menunjukkan jumlah UMKM per kecamatan</sub>",
            showlegend=False,
            margin=dict(l=0, r=0, t=60, b=0),
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
