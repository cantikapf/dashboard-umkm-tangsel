# GitHub Pages Setup Guide

## Steps to Deploy Dashboard to GitHub Pages

### 1. Create GitHub Repository
1. Go to GitHub and create a new repository
2. Name it something like `dashboard-umkm-tangsel`
3. Make it public (required for free GitHub Pages)

### 2. Upload Files
Upload these files to your repository:
- `docs/index.html` (the main dashboard file)
- `docs/README.md` (documentation)
- All other project files

### 3. Enable GitHub Pages
1. Go to your repository settings
2. Scroll down to "Pages" section
3. Under "Source", select "Deploy from a branch"
4. Choose "main" branch and "/docs" folder
5. Click "Save"

### 4. Access Your Dashboard
Your dashboard will be available at:
`https://[your-username].github.io/[repository-name]/`

### 5. Custom Domain (Optional)
If you have a custom domain:
1. Add a `CNAME` file in the docs folder with your domain
2. Configure DNS settings with your domain provider

## Files Structure for GitHub Pages
```
repository/
├── docs/
│   ├── index.html          # Main dashboard
│   └── README.md           # Documentation
├── umkm_tangerang_selatan_analysis/
│   ├── dashboard_umkm_static.py
│   ├── generate_static.py
│   └── data/
└── README.md
```

## Notes
- The dashboard is fully static and doesn't require a server
- All charts and interactions work client-side
- Mobile responsive design included
- Uses Bootstrap 5 and Plotly.js from CDN
