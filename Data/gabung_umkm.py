import pandas as pd
import os
from datetime import datetime

# Menggunakan path relatif ke folder Data saat ini
folder_path = '.'  # Folder saat ini (Data)
all_data = []

print("🔄 Memulai proses penggabungan data UMKM Tangerang Selatan...")
print("=" * 60)

for file in os.listdir(folder_path):
    if file.endswith('.csv'):
        bidang = os.path.splitext(file)[0]
        file_path = os.path.join(folder_path, file)

        try:
            # ✅ Lewati baris pertama (judul) dan beri nama kolom secara manual
            df = pd.read_csv(file_path, skiprows=2, sep=';', encoding='utf-8-sig', names=['Kecamatan', 'Mikro', 'Kecil'])
            df = df.dropna(subset=['Kecamatan'])  # hilangkan baris kosong
            df = df[df['Kecamatan'].str.lower() != 'kecamatan']  # buang header yang ikut masuk
            
            # Konversi ke numeric dan handle error
            df['Mikro'] = pd.to_numeric(df['Mikro'], errors='coerce').fillna(0).astype(int)
            df['Kecil'] = pd.to_numeric(df['Kecil'], errors='coerce').fillna(0).astype(int)
            
            # Tambahkan kolom bidang dan total
            df['Bidang'] = bidang
            df['Total'] = df['Mikro'] + df['Kecil']
            
            all_data.append(df)
            print(f"✅ {bidang:<20} → {len(df)} kecamatan, Total UMKM: {df['Total'].sum():,}")

        except Exception as e:
            print(f"❌ Error di file {file}: {e}")

# Gabungkan semua data
if all_data:
    print("\n🔄 Menggabungkan semua data...")
    gabungan = pd.concat(all_data, ignore_index=True)
    
    # Reorder kolom untuk kemudahan analisis
    gabungan = gabungan[['Kecamatan', 'Bidang', 'Mikro', 'Kecil', 'Total']]
    
    print(f"✅ Data berhasil digabung: {len(gabungan)} baris")
    print(f"📊 Total UMKM keseluruhan: {gabungan['Total'].sum():,}")
    
    # Buat Excel dengan multiple sheets untuk analisis
    with pd.ExcelWriter('UMKM_Tangerang_Selatan_Analisis.xlsx', engine='openpyxl') as writer:
        
        # Sheet 1: Data Lengkap
        gabungan.to_excel(writer, sheet_name='Data_Lengkap', index=False)
        
        # Sheet 2: Pivot - UMKM per Kecamatan per Bidang
        pivot_kecamatan_bidang = gabungan.pivot_table(
            index='Kecamatan', 
            columns='Bidang', 
            values='Total', 
            aggfunc='sum', 
            fill_value=0
        )
        pivot_kecamatan_bidang.to_excel(writer, sheet_name='Per_Kecamatan_Bidang')
        
        # Sheet 3: Ringkasan per Kecamatan
        ringkasan_kecamatan = gabungan.groupby('Kecamatan').agg({
            'Mikro': 'sum',
            'Kecil': 'sum', 
            'Total': 'sum'
        }).reset_index()
        ringkasan_kecamatan['Jumlah_Bidang'] = gabungan.groupby('Kecamatan')['Bidang'].nunique().values
        ringkasan_kecamatan = ringkasan_kecamatan.sort_values('Total', ascending=False)
        ringkasan_kecamatan.to_excel(writer, sheet_name='Ringkasan_Kecamatan', index=False)
        
        # Sheet 4: Ringkasan per Bidang
        ringkasan_bidang = gabungan.groupby('Bidang').agg({
            'Mikro': 'sum',
            'Kecil': 'sum',
            'Total': 'sum'
        }).reset_index()
        ringkasan_bidang = ringkasan_bidang.sort_values('Total', ascending=False)
        ringkasan_bidang.to_excel(writer, sheet_name='Ringkasan_Bidang', index=False)
        
        # Sheet 5: Top 10 Kombinasi Kecamatan-Bidang
        top_kombinasi = gabungan.nlargest(10, 'Total')[['Kecamatan', 'Bidang', 'Mikro', 'Kecil', 'Total']]
        top_kombinasi.to_excel(writer, sheet_name='Top_10_Kombinasi', index=False)
    
    print("\n📈 RINGKASAN ANALISIS")
    print("=" * 40)
    print(f"📍 Jumlah Kecamatan: {gabungan['Kecamatan'].nunique()}")
    print(f"🏢 Jumlah Bidang Usaha: {gabungan['Bidang'].nunique()}")
    print(f"🏪 Total UMKM Mikro: {gabungan['Mikro'].sum():,}")
    print(f"🏬 Total UMKM Kecil: {gabungan['Kecil'].sum():,}")
    print(f"🎯 TOTAL KESELURUHAN: {gabungan['Total'].sum():,}")
    
    print("\n🏆 TOP 3 KECAMATAN (berdasarkan jumlah UMKM):")
    top_kecamatan = ringkasan_kecamatan.head(3)
    for i, row in top_kecamatan.iterrows():
        print(f"   {row['Kecamatan']:<15}: {row['Total']:,} UMKM")
    
    print("\n🏆 TOP 3 BIDANG USAHA (berdasarkan jumlah UMKM):")
    top_bidang = ringkasan_bidang.head(3)
    for i, row in top_bidang.iterrows():
        print(f"   {row['Bidang']:<15}: {row['Total']:,} UMKM")
    
    print(f"\n✅ File Excel berhasil dibuat: 'UMKM_Tangerang_Selatan_Analisis.xlsx'")
    print(f"📅 Waktu pembuatan: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
else:
    print("\n❌ Tidak ada data valid yang berhasil digabung.")
