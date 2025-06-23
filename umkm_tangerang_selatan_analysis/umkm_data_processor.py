"""
🐍 UMKM Data Processor - Enhanced Analysis Engine
Processes UMKM data from multiple CSV files and creates comprehensive analysis
"""

import pandas as pd
import os
import json
from datetime import datetime
from pathlib import Path

class UMKMDataProcessor:
    def __init__(self, data_folder='data', output_folder='data_output'):
        self.data_folder = Path(data_folder)
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(exist_ok=True)
        
        # Tangerang Selatan districts
        self.kecamatan_list = [
            'Ciputat', 'Ciputat Timur', 'Pamulang', 'Pondok Aren',
            'Serpong', 'Serpong Utara', 'Setu'
        ]
        
        self.all_data = []
        self.processed_data = None
        
    def load_csv_files(self):
        """Load and process all CSV files from data folder"""
        print("🔄 Memulai proses penggabungan data UMKM Tangerang Selatan...")
        print("=" * 60)
        
        csv_files = list(self.data_folder.glob('*.csv'))
        
        if not csv_files:
            print(f"❌ Tidak ada file CSV ditemukan di folder {self.data_folder}")
            return False
            
        for file_path in csv_files:
            bidang = file_path.stem
            
            try:
                # Enhanced CSV reading with better error handling
                df = pd.read_csv(
                    file_path, 
                    skiprows=2, 
                    sep=';', 
                    encoding='utf-8-sig', 
                    names=['Kecamatan', 'Mikro', 'Kecil']
                )
                
                # Data cleaning
                df = df.dropna(subset=['Kecamatan'])
                df = df[df['Kecamatan'].str.lower() != 'kecamatan']
                df['Kecamatan'] = df['Kecamatan'].str.strip()
                
                # Convert to numeric with better error handling
                df['Mikro'] = pd.to_numeric(df['Mikro'], errors='coerce').fillna(0).astype(int)
                df['Kecil'] = pd.to_numeric(df['Kecil'], errors='coerce').fillna(0).astype(int)
                
                # Add calculated columns
                df['Bidang'] = bidang
                df['Total'] = df['Mikro'] + df['Kecil']
                
                # Validate districts
                valid_districts = df[df['Kecamatan'].isin(self.kecamatan_list)]
                invalid_districts = df[~df['Kecamatan'].isin(self.kecamatan_list)]
                
                if len(invalid_districts) > 0:
                    print(f"⚠️  {bidang}: {len(invalid_districts)} kecamatan tidak dikenali")
                
                self.all_data.append(df)
                print(f"✅ {bidang:<20} → {len(df)} kecamatan, Total UMKM: {df['Total'].sum():,}")
                
            except Exception as e:
                print(f"❌ Error di file {file_path.name}: {e}")
                
        return len(self.all_data) > 0
    
    def process_data(self):
        """Process and combine all loaded data"""
        if not self.all_data:
            print("❌ Tidak ada data untuk diproses")
            return False
            
        print("\n🔄 Menggabungkan semua data...")
        self.processed_data = pd.concat(self.all_data, ignore_index=True)
        
        # Reorder columns
        self.processed_data = self.processed_data[['Kecamatan', 'Bidang', 'Mikro', 'Kecil', 'Total']]
        
        print(f"✅ Data berhasil digabung: {len(self.processed_data)} baris")
        print(f"📊 Total UMKM keseluruhan: {self.processed_data['Total'].sum():,}")
        
        return True
    
    def create_analysis_views(self):
        """Create various analysis views of the data"""
        if self.processed_data is None:
            print("❌ Data belum diproses")
            return {}
            
        analysis = {}
        
        # 1. Pivot table - UMKM per Kecamatan per Bidang
        analysis['pivot_kecamatan_bidang'] = self.processed_data.pivot_table(
            index='Kecamatan', 
            columns='Bidang', 
            values='Total', 
            aggfunc='sum', 
            fill_value=0
        )
        
        # 2. Summary per Kecamatan
        analysis['ringkasan_kecamatan'] = self.processed_data.groupby('Kecamatan').agg({
            'Mikro': 'sum',
            'Kecil': 'sum', 
            'Total': 'sum'
        }).reset_index()
        analysis['ringkasan_kecamatan']['Jumlah_Bidang'] = (
            self.processed_data.groupby('Kecamatan')['Bidang'].nunique().values
        )
        analysis['ringkasan_kecamatan'] = analysis['ringkasan_kecamatan'].sort_values('Total', ascending=False)
        
        # 3. Summary per Bidang
        analysis['ringkasan_bidang'] = self.processed_data.groupby('Bidang').agg({
            'Mikro': 'sum',
            'Kecil': 'sum',
            'Total': 'sum'
        }).reset_index()
        analysis['ringkasan_bidang'] = analysis['ringkasan_bidang'].sort_values('Total', ascending=False)
        
        # 4. Top combinations
        analysis['top_kombinasi'] = self.processed_data.nlargest(10, 'Total')[
            ['Kecamatan', 'Bidang', 'Mikro', 'Kecil', 'Total']
        ]
        
        # 5. Statistics summary
        analysis['statistik'] = {
            'total_umkm': int(self.processed_data['Total'].sum()),
            'total_mikro': int(self.processed_data['Mikro'].sum()),
            'total_kecil': int(self.processed_data['Kecil'].sum()),
            'jumlah_kecamatan': self.processed_data['Kecamatan'].nunique(),
            'jumlah_bidang': self.processed_data['Bidang'].nunique(),
            'rata_rata_per_kecamatan': float(self.processed_data.groupby('Kecamatan')['Total'].sum().mean()),
            'rata_rata_per_bidang': float(self.processed_data.groupby('Bidang')['Total'].sum().mean())
        }
        
        return analysis
    
    def save_excel_analysis(self, filename='UMKM_Tangerang_Selatan_Analisis.xlsx'):
        """Save comprehensive Excel analysis"""
        analysis = self.create_analysis_views()
        
        if not analysis:
            return False
            
        excel_path = self.output_folder / filename
        
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            # Sheet 1: Raw data
            self.processed_data.to_excel(writer, sheet_name='Data_Lengkap', index=False)
            
            # Sheet 2: Pivot table
            analysis['pivot_kecamatan_bidang'].to_excel(writer, sheet_name='Per_Kecamatan_Bidang')
            
            # Sheet 3: District summary
            analysis['ringkasan_kecamatan'].to_excel(writer, sheet_name='Ringkasan_Kecamatan', index=False)
            
            # Sheet 4: Sector summary
            analysis['ringkasan_bidang'].to_excel(writer, sheet_name='Ringkasan_Bidang', index=False)
            
            # Sheet 5: Top combinations
            analysis['top_kombinasi'].to_excel(writer, sheet_name='Top_10_Kombinasi', index=False)
        
        print(f"✅ File Excel berhasil dibuat: '{excel_path}'")
        return True
    
    def save_json_data(self, filename='umkm_data.json'):
        """Save processed data as JSON for dashboard"""
        analysis = self.create_analysis_views()
        
        if not analysis:
            return False
            
        # Convert DataFrames to JSON-serializable format
        json_data = {
            'data_lengkap': self.processed_data.to_dict('records'),
            'ringkasan_kecamatan': analysis['ringkasan_kecamatan'].to_dict('records'),
            'ringkasan_bidang': analysis['ringkasan_bidang'].to_dict('records'),
            'top_kombinasi': analysis['top_kombinasi'].to_dict('records'),
            'statistik': analysis['statistik'],
            'pivot_data': analysis['pivot_kecamatan_bidang'].to_dict('index'),
            'metadata': {
                'last_updated': datetime.now().isoformat(),
                'total_records': len(self.processed_data),
                'kecamatan_list': self.kecamatan_list
            }
        }
        
        json_path = self.output_folder / filename
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
            
        print(f"✅ File JSON berhasil dibuat: '{json_path}'")
        return True
    
    def print_summary(self):
        """Print comprehensive analysis summary"""
        if self.processed_data is None:
            print("❌ Data belum diproses")
            return
            
        analysis = self.create_analysis_views()
        stats = analysis['statistik']
        
        print("\n📈 RINGKASAN ANALISIS UMKM TANGERANG SELATAN")
        print("=" * 50)
        print(f"📍 Jumlah Kecamatan: {stats['jumlah_kecamatan']}")
        print(f"🏢 Jumlah Bidang Usaha: {stats['jumlah_bidang']}")
        print(f"🏪 Total UMKM Mikro: {stats['total_mikro']:,}")
        print(f"🏬 Total UMKM Kecil: {stats['total_kecil']:,}")
        print(f"🎯 TOTAL KESELURUHAN: {stats['total_umkm']:,}")
        print(f"📊 Rata-rata per Kecamatan: {stats['rata_rata_per_kecamatan']:.1f}")
        print(f"📊 Rata-rata per Bidang: {stats['rata_rata_per_bidang']:.1f}")
        
        print("\n🏆 TOP 3 KECAMATAN (berdasarkan jumlah UMKM):")
        top_kecamatan = analysis['ringkasan_kecamatan'].head(3)
        for i, row in top_kecamatan.iterrows():
            print(f"   {row['Kecamatan']:<15}: {row['Total']:,} UMKM")
        
        print("\n🏆 TOP 3 BIDANG USAHA (berdasarkan jumlah UMKM):")
        top_bidang = analysis['ringkasan_bidang'].head(3)
        for i, row in top_bidang.iterrows():
            print(f"   {row['Bidang']:<15}: {row['Total']:,} UMKM")
        
        print(f"\n📅 Waktu analisis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    """Main execution function"""
    processor = UMKMDataProcessor()
    
    # Load and process data
    if processor.load_csv_files():
        if processor.process_data():
            # Save outputs
            processor.save_excel_analysis()
            processor.save_json_data()
            processor.print_summary()
        else:
            print("❌ Gagal memproses data")
    else:
        print("❌ Gagal memuat file CSV")

if __name__ == "__main__":
    main()
