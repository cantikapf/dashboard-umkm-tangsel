import os
from pathlib import Path
from dashboard_umkm_static import UMKMStaticDashboard

# Change to the script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Create docs directory if it doesn't exist
docs_dir = Path('docs')
docs_dir.mkdir(exist_ok=True)

# Generate static dashboard
dashboard = UMKMStaticDashboard()
dashboard.generate_html(str(docs_dir / 'index.html'))
