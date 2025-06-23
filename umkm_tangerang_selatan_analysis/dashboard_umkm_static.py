"""
📈 UMKM Dashboard - Static HTML Generator
Generates a static HTML dashboard for GitHub Pages
"""

import json
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo
from pathlib import Path

class UMKMStaticDashboard:
    def __init__(self, data_path='data_output/umkm_data.json'):
        """Initialize dashboard with data"""
        self.data_path = Path(data_path)
        self.load_data()
        
    def load_data(self):
        """Load data from JSON file"""
        with open(self.data_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
            
        # Convert to DataFrames for easier manipulation
        self.df = pd.DataFrame(self.data['data_lengkap'])
        self.df_kecamatan = pd.DataFrame(self.data['ringkasan_kecamatan'])
        self.df_bidang = pd.DataFrame(self.data['ringkasan_bidang'])
        
    def create_overview_stats(self):
        """Create overview statistics HTML"""
        stats = self.data['statistik']
        
        return f"""
        <div class="row mb-4">
            <div class="col-md-4">
                <div class="card mb-4">
                    <div class="card-body text-center">
                        <h4 class="card-title">Total UMKM</h4>
                        <h2 class="card-text text-primary">{stats['total_umkm']:,}</h2>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card mb-4">
                    <div class="card-body text-center">
                        <h4 class="card-title">UMKM Mikro</h4>
                        <h2 class="card-text text-success">{stats['total_mikro']:,}</h2>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card mb-4">
                    <div class="card-body text-center">
                        <h4 class="card-title">UMKM Kecil</h4>
                        <h2 class="card-text text-info">{stats['total_kecil']:,}</h2>
                    </div>
                </div>
            </div>
        </div>
        """
    
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
        
        return fig
    
    def create_district_chart(self):
        """Create district distribution chart"""
        fig = px.bar(
            self.df_kecamatan,
            x='Kecamatan',
            y='Total',
            title='Distribusi UMKM per Kecamatan',
            color='Total',
            color_continuous_scale='viridis',
            hover_data={'Total': ':,'}
        )
        
        fig.update_traces(
            hovertemplate='<b>%{x}</b><br>Total UMKM: %{y:,}<extra></extra>'
        )
        
        fig.update_layout(
            xaxis_title='Kecamatan',
            yaxis_title='Jumlah UMKM',
            height=400,
            margin=dict(l=0, r=0, t=60, b=0)
        )
        
        return fig
    
    def create_business_type_chart(self):
        """Create business type distribution chart"""
        fig = px.pie(
            self.df_bidang,
            values='Total',
            names='Bidang',
            title='Distribusi UMKM berdasarkan Bidang Usaha'
        )
        
        fig.update_layout(
            height=400,
            margin=dict(l=0, r=0, t=60, b=0)
        )
        
        return fig
    
    def generate_html(self, output_path='index.html'):
        """Generate static HTML dashboard"""
        
        # Create charts
        geomap = self.create_geomap()
        district_chart = self.create_district_chart()
        business_chart = self.create_business_type_chart()
        
        # Convert charts to HTML
        geomap_html = pyo.plot(geomap, output_type='div', include_plotlyjs=False)
        district_chart_html = pyo.plot(district_chart, output_type='div', include_plotlyjs=False)
        business_chart_html = pyo.plot(business_chart, output_type='div', include_plotlyjs=False)
        
        # Create complete HTML
        html_content = f"""
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard UMKM Tangerang Selatan</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Plotly.js -->
    <script src="https://cdn.plot.ly/plotly-2.26.0.min.js"></script>
    
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f8f9fa;
        }}
        
        .dashboard-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem 0;
            margin-bottom: 2rem;
        }}
        
        .card {{
            border: none;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }}
        
        .card:hover {{
            transform: translateY(-5px);
        }}
        
        .chart-container {{
            background: white;
            border-radius: 15px;
            padding: 1rem;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        
        .footer {{
            background-color: #343a40;
            color: white;
            padding: 2rem 0;
            margin-top: 3rem;
        }}
        
        @media (max-width: 768px) {{
            .dashboard-header h1 {{
                font-size: 1.8rem;
            }}
            
            .card h2 {{
                font-size: 1.5rem;
            }}
        }}
    </style>
</head>
<body>
    <!-- Header -->
    <div class="dashboard-header">
        <div class="container">
            <h1 class="text-center mb-0">Dashboard UMKM Tangerang Selatan</h1>
            <p class="text-center mb-0 mt-2">Visualisasi Data Usaha Mikro, Kecil, dan Menengah</p>
        </div>
    </div>
    
    <!-- Main Content -->
    <div class="container-fluid">
        <!-- Overview Statistics -->
        {self.create_overview_stats()}
        
        <!-- Geographic Map -->
        <div class="row mb-4">
            <div class="col-12">
                <div class="chart-container">
                    {geomap_html}
                </div>
            </div>
        </div>
        
        <!-- Charts Row -->
        <div class="row mb-4">
            <div class="col-lg-6 mb-4">
                <div class="chart-container">
                    {district_chart_html}
                </div>
            </div>
            <div class="col-lg-6 mb-4">
                <div class="chart-container">
                    {business_chart_html}
                </div>
            </div>
        </div>
        
        <!-- Data Summary Table -->
        <div class="row mb-4">
            <div class="col-12">
                <div class="chart-container">
                    <h4 class="mb-3">Ringkasan Data per Kecamatan</h4>
                    <div class="table-responsive">
                        <table class="table table-striped table-hover">
                            <thead class="table-dark">
                                <tr>
                                    <th>Kecamatan</th>
                                    <th>Total UMKM</th>
                                    <th>Mikro</th>
                                    <th>Kecil</th>
                                    <th>Persentase</th>
                                </tr>
                            </thead>
                            <tbody>
"""
        
        # Add table rows
        total_umkm = self.df_kecamatan['Total'].sum()
        for _, row in self.df_kecamatan.iterrows():
            percentage = (row['Total'] / total_umkm) * 100
            html_content += f"""
                                <tr>
                                    <td><strong>{row['Kecamatan']}</strong></td>
                                    <td>{row['Total']:,}</td>
                                    <td>{row['Mikro']:,}</td>
                                    <td>{row['Kecil']:,}</td>
                                    <td>{percentage:.1f}%</td>
                                </tr>
"""
        
        html_content += f"""
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <h5>Dashboard UMKM Tangsel</h5>
                    <p>Visualisasi data UMKM Kota Tangerang Selatan untuk mendukung pengembangan ekonomi lokal.</p>
                </div>
                <div class="col-md-6 text-md-end">
                    <p class="mb-0">Last updated: {self.data['metadata']['last_updated']}</p>
                    <p class="mb-0"><small>Data source: Dinas Koperasi dan UMKM Kota Tangerang Selatan</small></p>
                </div>
            </div>
        </div>
    </footer>
    
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    
    <script>
        // Make charts responsive
        window.addEventListener('resize', function() {{
            Plotly.Plots.resize();
        }});
        
        // Add smooth scrolling
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({{
                    behavior: 'smooth'
                }});
            }});
        }});
    </script>
</body>
</html>
"""
        
        # Write HTML file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Static HTML dashboard generated: {output_path}")
        return output_path

def main():
    """Main execution function"""
    dashboard = UMKMStaticDashboard()
    dashboard.generate_html('index.html')

if __name__ == "__main__":
    main()
