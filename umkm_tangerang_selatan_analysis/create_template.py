"""
📋 Create Template - Excel Template Generator
Creates standardized Excel templates for UMKM data collection
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

class TemplateGenerator:
    def __init__(self, template_folder='templates'):
        self.template_folder = Path(template_folder)
        self.template_folder.mkdir(exist_ok=True)
        
        # Standard districts in Tangerang Selatan
        self.kecamatan_list = [
            'Ciputat',
            'Ciputat Timur', 
            'Pamulang',
            'Pondok Aren',
            'Serpong',
            'Serpong Utara',
            'Setu'
        ]
        
        # Standard business sectors
        self.bidang_usaha = [
            'Agrobisnis', 'Akomodasi', 'Aksesori', 'Ekspedisi', 'Elektronik',
            'Farmasi', 'Fashion', 'Furniture', 'Jasa', 'Konter HP',
            'Konveksi', 'Kreatif', 'Kuliner', 'Lainnya', 'Otomotif',
            'Pendidikan', 'Perawatan Kesehatan', 'Perikanan', 'Pertanian',
            'Sayur Buah', 'Teknologi', 'Toko Sembako', 'Transportasi'
        ]
    
    def create_csv_template(self, bidang_usaha):
        """Create CSV template for specific business sector"""
        template_data = {
            'Kecamatan': self.kecamatan_list,
            'Mikro': [0] * len(self.kecamatan_list),
            'Kecil': [0] * len(self.kecamatan_list)
        }
        
        df = pd.DataFrame(template_data)
        
        # Create filename
        filename = f"{bidang_usaha}.csv"
        filepath = self.template_folder / filename
        
        # Save with proper formatting
        with open(filepath, 'w', encoding='utf-8-sig') as f:
            # Write header
            f.write(f"DATA UMKM {bidang_usaha.upper()} - TANGERANG SELATAN\n")
            f.write(f"Tanggal: {datetime.now().strftime('%Y-%m-%d')}\n")
            
            # Write data
            df.to_csv(f, sep=';', index=False)
        
        return filepath
    
    def create_all_csv_templates(self):
        """Create CSV templates for all business sectors"""
        print("📋 MEMBUAT TEMPLATE CSV UNTUK SEMUA BIDANG USAHA")
        print("=" * 60)
        
        created_files = []
        
        for bidang in self.bidang_usaha:
            try:
                filepath = self.create_csv_template(bidang)
                created_files.append(filepath)
                print(f"✅ {bidang:<20} → {filepath.name}")
            except Exception as e:
                print(f"❌ Error creating template for {bidang}: {e}")
        
        print(f"\n✅ {len(created_files)} template CSV berhasil dibuat")
        return created_files
    
    def create_excel_master_template(self):
        """Create comprehensive Excel template with all sectors"""
        print("\n📊 MEMBUAT MASTER TEMPLATE EXCEL")
        print("=" * 40)
        
        filename = "UMKM_Master_Template.xlsx"
        filepath = self.template_folder / filename
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # Sheet 1: Instructions
            instructions = pd.DataFrame({
                'PETUNJUK PENGGUNAAN TEMPLATE UMKM TANGERANG SELATAN': [
                    '1. Template ini digunakan untuk mengumpulkan data UMKM per kecamatan',
                    '2. Setiap sheet mewakili satu bidang usaha',
                    '3. Isi kolom Mikro dan Kecil dengan jumlah UMKM yang sesuai',
                    '4. Pastikan data yang diisi adalah angka (bukan teks)',
                    '5. Jangan mengubah nama kecamatan yang sudah ada',
                    '6. Simpan file setelah selesai mengisi data',
                    '',
                    f'Template dibuat pada: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
                    'Untuk pertanyaan, hubungi tim analisis data'
                ]
            })
            instructions.to_excel(writer, sheet_name='PETUNJUK', index=False)
            
            # Sheet 2: Summary template
            summary_template = pd.DataFrame({
                'Kecamatan': self.kecamatan_list,
                'Total_Mikro': [0] * len(self.kecamatan_list),
                'Total_Kecil': [0] * len(self.kecamatan_list),
                'Total_UMKM': [0] * len(self.kecamatan_list),
                'Jumlah_Bidang': [0] * len(self.kecamatan_list)
            })
            summary_template.to_excel(writer, sheet_name='RINGKASAN', index=False)
            
            # Sheets for each business sector
            for bidang in self.bidang_usaha:
                template_data = pd.DataFrame({
                    'Kecamatan': self.kecamatan_list,
                    'Mikro': [0] * len(self.kecamatan_list),
                    'Kecil': [0] * len(self.kecamatan_list)
                })
                
                # Limit sheet name to 31 characters (Excel limitation)
                sheet_name = bidang[:31] if len(bidang) > 31 else bidang
                template_data.to_excel(writer, sheet_name=sheet_name, index=False)
        
        print(f"✅ Master template Excel berhasil dibuat: {filepath}")
        return filepath
    
    def create_validation_template(self):
        """Create data validation template"""
        print("\n🔍 MEMBUAT TEMPLATE VALIDASI DATA")
        print("=" * 40)
        
        filename = "UMKM_Validation_Template.xlsx"
        filepath = self.template_folder / filename
        
        # Create validation rules
        validation_data = {
            'Field': ['Kecamatan', 'Bidang_Usaha', 'Mikro', 'Kecil'],
            'Type': ['Text', 'Text', 'Number', 'Number'],
            'Required': ['Yes', 'Yes', 'Yes', 'Yes'],
            'Valid_Values': [
                '; '.join(self.kecamatan_list),
                '; '.join(self.bidang_usaha),
                'Integer >= 0',
                'Integer >= 0'
            ],
            'Description': [
                'Nama kecamatan di Tangerang Selatan',
                'Bidang usaha UMKM',
                'Jumlah UMKM kategori Mikro',
                'Jumlah UMKM kategori Kecil'
            ]
        }
        
        df_validation = pd.DataFrame(validation_data)
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            df_validation.to_excel(writer, sheet_name='Validation_Rules', index=False)
            
            # Add sample data
            sample_data = pd.DataFrame({
                'Kecamatan': self.kecamatan_list[:3],
                'Bidang_Usaha': ['Kuliner', 'Fashion', 'Teknologi'],
                'Mikro': [150, 75, 25],
                'Kecil': [30, 15, 10]
            })
            sample_data.to_excel(writer, sheet_name='Sample_Data', index=False)
        
        print(f"✅ Template validasi berhasil dibuat: {filepath}")
        return filepath
    
    def create_all_templates(self):
        """Create all types of templates"""
        print("🎯 MEMBUAT SEMUA TEMPLATE UMKM")
        print("=" * 50)
        print(f"Folder template: {self.template_folder.absolute()}")
        
        created_files = []
        
        # Create CSV templates
        csv_files = self.create_all_csv_templates()
        created_files.extend(csv_files)
        
        # Create Excel master template
        excel_file = self.create_excel_master_template()
        created_files.append(excel_file)
        
        # Create validation template
        validation_file = self.create_validation_template()
        created_files.append(validation_file)
        
        print(f"\n🎉 SEMUA TEMPLATE BERHASIL DIBUAT!")
        print(f"📁 Total file: {len(created_files)}")
        print(f"📂 Lokasi: {self.template_folder.absolute()}")
        
        return created_files

def main():
    """Main execution function"""
    generator = TemplateGenerator()
    generator.create_all_templates()

if __name__ == "__main__":
    main()
