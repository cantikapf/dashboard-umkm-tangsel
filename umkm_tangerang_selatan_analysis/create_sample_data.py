"""
🔧 Create Sample Data - Sample Data Generator
Creates sample UMKM data for testing and development
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import random

class SampleDataGenerator:
    def __init__(self, data_folder='data'):
        self.data_folder = Path(data_folder)
        self.data_folder.mkdir(exist_ok=True)
        
        # Standard districts in Tangerang Selatan
        self.kecamatan_list = [
            'Ciputat', 'Ciputat Timur', 'Pamulang', 'Pondok Aren',
            'Serpong', 'Serpong Utara', 'Setu'
        ]
        
        # Standard business sectors with typical distribution weights
        self.bidang_weights = {
            'Kuliner': 0.20,        # Food businesses are typically most common
            'Fashion': 0.15,        # Fashion is usually second
            'Toko Sembako': 0.12,   # Essential goods stores
            'Jasa': 0.10,          # Services
            'Kreatif': 0.08,       # Creative industries
            'Teknologi': 0.07,      # Tech businesses
            'Otomotif': 0.05,       # Automotive
            'Furniture': 0.05,      # Furniture
            'Farmasi': 0.04,        # Pharmacy
            'Pendidikan': 0.04,     # Education
            'Elektronik': 0.03,     # Electronics
            'Konveksi': 0.02,       # Clothing manufacture
            'Agrobisnis': 0.01,     # Agribusiness
            'Perikanan': 0.01,      # Fishery
            'Pertanian': 0.01,      # Agriculture
            'Sayur Buah': 0.01,     # Fruits and vegetables
            'Aksesori': 0.01,       # Accessories
            'Akomodasi': 0.01       # Accommodation
        }
    
    def generate_realistic_distribution(self, total, micro_ratio=0.8):
        """Generate realistic distribution between micro and small businesses"""
        micro = int(total * micro_ratio)
        small = total - micro
        return micro, small
    
    def create_sample_data(self, base_total=1000):
        """Create sample data for each business sector"""
        print("🔧 MEMBUAT DATA SAMPEL UMKM")
        print("=" * 50)
        
        created_files = []
        
        for bidang, weight in self.bidang_weights.items():
            try:
                # Calculate total UMKMs for this sector
                sector_total = int(base_total * weight)
                
                # Create sample data for each district
                data = []
                for kecamatan in self.kecamatan_list:
                    # Add some randomness to distribution
                    district_total = int(sector_total * (1 + random.uniform(-0.3, 0.3)))
                    micro, small = self.generate_realistic_distribution(district_total)
                    
                    data.append({
                        'Kecamatan': kecamatan,
                        'Mikro': micro,
                        'Kecil': small
                    })
                
                df = pd.DataFrame(data)
                
                # Save to CSV
                filename = f"{bidang}.csv"
                filepath = self.data_folder / filename
                
                with open(filepath, 'w', encoding='utf-8-sig') as f:
                    f.write(f"DATA UMKM {bidang.upper()} - TANGERANG SELATAN\n")
                    f.write(f"Tanggal: {datetime.now().strftime('%Y-%m-%d')}\n")
                    df.to_csv(f, sep=';', index=False)
                
                created_files.append(filepath)
                print(f"✅ {bidang:<20} → {filepath.name}")
                
            except Exception as e:
                print(f"❌ Error creating sample data for {bidang}: {e}")
        
        print(f"\n✅ {len(created_files)} file data sampel berhasil dibuat")
        print(f"📂 Lokasi: {self.data_folder.absolute()}")
        
        return created_files
    
    def create_summary(self):
        """Create a summary of the generated sample data"""
        all_data = []
        
        for file in self.data_folder.glob('*.csv'):
            try:
                df = pd.read_csv(file, skiprows=2, sep=';')
                bidang = file.stem
                df['Bidang'] = bidang
                all_data.append(df)
            except Exception:
                continue
        
        if all_data:
            combined = pd.concat(all_data, ignore_index=True)
            
            print("\n📊 RINGKASAN DATA SAMPEL")
            print("=" * 30)
            print(f"Total UMKM: {combined['Mikro'].sum() + combined['Kecil'].sum():,}")
            print(f"Total Mikro: {combined['Mikro'].sum():,}")
            print(f"Total Kecil: {combined['Kecil'].sum():,}")
            print("\nDistribusi per Kecamatan:")
            
            district_summary = combined.groupby('Kecamatan').agg({
                'Mikro': 'sum',
                'Kecil': 'sum'
            })
            district_summary['Total'] = district_summary['Mikro'] + district_summary['Kecil']
            print(district_summary.sort_values('Total', ascending=False))

def main():
    """Main execution function"""
    generator = SampleDataGenerator()
    generator.create_sample_data()
    generator.create_summary()

if __name__ == "__main__":
    main()
