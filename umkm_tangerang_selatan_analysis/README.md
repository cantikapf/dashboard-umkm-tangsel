# 📊 Dashboard UMKM Tangerang Selatan

Dashboard interaktif untuk analisis data Usaha Mikro, Kecil, dan Menengah (UMKM) di Tangerang Selatan dengan visualisasi data dan peta geografis per kecamatan.

## 🎯 Fitur Utama

- **📈 Visualisasi Interaktif**: Charts dan grafik yang responsif
- **🗺️ Peta Geografis**: Distribusi UMKM per kecamatan di Tangerang Selatan
- **📊 Analisis Komprehensif**: Ringkasan statistik dan tren data
- **🔄 Pemrosesan Data Otomatis**: Pengolahan data dari multiple CSV files
- **📋 Template Generator**: Pembuat template untuk pengumpulan data
- **🚀 One-Click Deployment**: Menjalankan seluruh sistem dengan satu perintah

## 📁 Struktur Proyek

```
umkm_tangerang_selatan_analysis/
├── 🐍 umkm_data_processor.py   # Main analysis engine
├── 📈 dashboard_umkm.py        # Interactive web dashboard  
├── 🚀 run_all.py              # One-click automation
├── 📋 create_template.py       # Template generator
├── 🔧 create_sample_data.py    # Sample data creator
├── 📄 requirements.txt         # Dependencies
├── 📖 README.md               # Complete documentation
├── 📂 data/                   # Your CSV files go here
├── 📂 data_output/            # Analysis results
└── 📂 templates/              # Excel templates
```

## 🚀 Quick Start

### 1. Instalasi Dependencies

```bash
pip install -r requirements.txt
```

### 2. Persiapan Data

Letakkan file CSV UMKM Anda di folder `data/`. Format yang diharapkan:

```csv
DATA UMKM [BIDANG_USAHA] - TANGERANG SELATAN
Tanggal: 2024-01-01
Kecamatan;Mikro;Kecil
Ciputat;150;30
Ciputat Timur;120;25
...
```

### 3. Jalankan Dashboard

```bash
python run_all.py
```

Dashboard akan tersedia di: `http://localhost:8050`

## 📋 Penggunaan Detail

### Data Processor (`umkm_data_processor.py`)

```python
from umkm_data_processor import UMKMDataProcessor

# Inisialisasi processor
processor = UMKMDataProcessor(
    data_folder='data',
    output_folder='data_output'
)

# Load dan proses data
if processor.load_csv_files():
    processor.process_data()
    processor.save_excel_analysis()
    processor.save_json_data()
    processor.print_summary()
```

### Dashboard (`dashboard_umkm.py`)

```python
from dashboard_umkm import UMKMDashboard

# Inisialisasi dashboard
dashboard = UMKMDashboard(data_path='data_output/umkm_data.json')

# Jalankan server
dashboard.run_server(port=8050)
```

### Template Generator (`create_template.py`)

```python
from create_template import TemplateGenerator

# Buat semua template
generator = TemplateGenerator()
generator.create_all_templates()
```

### Sample Data Creator (`create_sample_data.py`)

```python
from create_sample_data import SampleDataGenerator

# Buat data sampel untuk testing
generator = SampleDataGenerator()
generator.create_sample_data()
```

## 📊 Fitur Dashboard

### 1. Overview Statistics
- Total UMKM keseluruhan
- Distribusi Mikro vs Kecil
- Jumlah kecamatan dan bidang usaha

### 2. Visualisasi Data
- **Bar Chart**: Distribusi UMKM per kecamatan
- **Pie Chart**: Distribusi per bidang usaha
- **Stacked Chart**: Kombinasi kecamatan-bidang
- **Geographic Map**: Peta Tangerang Selatan dengan data UMKM

### 3. Filter Interaktif
- Filter berdasarkan kecamatan
- Filter berdasarkan bidang usaha
- Real-time update visualisasi

## 🗺️ Data Geografis

Dashboard mencakup 7 kecamatan di Tangerang Selatan:

1. **Ciputat**
2. **Ciputat Timur**
3. **Pamulang**
4. **Pondok Aren**
5. **Serpong**
6. **Serpong Utara**
7. **Setu**

## 📈 Bidang Usaha yang Didukung

- Agrobisnis
- Akomodasi
- Aksesori
- Ekspedisi
- Elektronik
- Farmasi
- Fashion
- Furniture
- Jasa
- Konter HP
- Konveksi
- Kreatif
- Kuliner
- Lainnya
- Otomotif
- Pendidikan
- Perawatan Kesehatan
- Perikanan
- Pertanian
- Sayur Buah
- Teknologi
- Toko Sembako
- Transportasi

## 🔧 Konfigurasi

### Environment Variables

```bash
# Port untuk dashboard (default: 8050)
DASHBOARD_PORT=8050

# Debug mode (default: True)
DEBUG_MODE=True

# Data folder path
DATA_FOLDER=data

# Output folder path
OUTPUT_FOLDER=data_output
```

### Customization

Untuk menyesuaikan dashboard:

1. **Warna dan Theme**: Edit `dashboard_umkm.py` bagian styling
2. **Kecamatan**: Modifikasi `kecamatan_list` di `umkm_data_processor.py`
3. **Bidang Usaha**: Update `bidang_usaha` di `create_template.py`

## 📤 Output Files

### Excel Analysis (`data_output/UMKM_Tangerang_Selatan_Analisis.xlsx`)

- **Data_Lengkap**: Raw data gabungan
- **Per_Kecamatan_Bidang**: Pivot table
- **Ringkasan_Kecamatan**: Summary per kecamatan
- **Ringkasan_Bidang**: Summary per bidang usaha
- **Top_10_Kombinasi**: Top kombinasi kecamatan-bidang

### JSON Data (`data_output/umkm_data.json`)

```json
{
  "data_lengkap": [...],
  "ringkasan_kecamatan": [...],
  "ringkasan_bidang": [...],
  "statistik": {
    "total_umkm": 12345,
    "total_mikro": 9876,
    "total_kecil": 2469
  },
  "metadata": {
    "last_updated": "2024-01-01T12:00:00",
    "kecamatan_list": [...]
  }
}
```

## 🚀 Deployment

### Local Development

```bash
python run_all.py
```

### Production Deployment

```bash
# Menggunakan Gunicorn
gunicorn -w 4 -b 0.0.0.0:8050 dashboard_umkm:app

# Atau menggunakan Docker
docker build -t umkm-dashboard .
docker run -p 8050:8050 umkm-dashboard
```

### Cloud Deployment

Dashboard dapat di-deploy ke:
- **Heroku**: Gunakan `Procfile`
- **AWS EC2**: Setup dengan nginx + gunicorn
- **Google Cloud Run**: Containerized deployment
- **Azure App Service**: Python web app

## 🔍 Troubleshooting

### Common Issues

1. **File CSV tidak terbaca**
   ```
   Pastikan format encoding UTF-8-sig dan separator ';'
   ```

2. **Dashboard tidak muncul**
   ```
   Periksa port 8050 tidak digunakan aplikasi lain
   ```

3. **Error saat install dependencies**
   ```
   pip install --upgrade pip
   pip install -r requirements.txt --no-cache-dir
   ```

### Debug Mode

Aktifkan debug mode untuk troubleshooting:

```python
dashboard.run_server(debug=True, port=8050)
```

## 📝 Contributing

1. Fork repository
2. Buat feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 👥 Contact

- **Developer**: Tim Analisis Data
- **Email**: data@tangerangselatankota.go.id
- **Project Link**: [https://github.com/tangsel/umkm-dashboard](https://github.com/tangsel/umkm-dashboard)

## 🙏 Acknowledgments

- Data UMKM Tangerang Selatan
- Plotly Dash Community
- Bootstrap Components
- OpenStreetMap untuk data geografis

---

**📊 Dashboard UMKM Tangerang Selatan** - Membantu analisis dan visualisasi data UMKM untuk pengambilan keputusan yang lebih baik.
