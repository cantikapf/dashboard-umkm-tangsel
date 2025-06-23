import pandas as pd
import openpyxl

print("🔍 VERIFIKASI FILE EXCEL ANALISIS UMKM")
print("=" * 50)

try:
    # Baca file Excel
    excel_file = 'UMKM_Tangerang_Selatan_Analisis.xlsx'
    
    # Cek semua sheet yang ada
    workbook = openpyxl.load_workbook(excel_file)
    sheet_names = workbook.sheetnames
    
    print(f"📋 Sheet yang tersedia: {len(sheet_names)}")
    for i, sheet in enumerate(sheet_names, 1):
        print(f"   {i}. {sheet}")
    
    print("\n" + "=" * 50)
    
    # Verifikasi setiap sheet
    for sheet_name in sheet_names:
        print(f"\n📊 SHEET: {sheet_name}")
        print("-" * 30)
        
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        print(f"   Jumlah baris: {len(df)}")
        print(f"   Jumlah kolom: {len(df.columns)}")
        print(f"   Kolom: {list(df.columns)}")
        
        if len(df) > 0:
            print(f"   Preview data (5 baris pertama):")
            print(df.head().to_string(index=False))
        
        print()
    
    # Verifikasi data spesifik
    print("\n🎯 VERIFIKASI DATA SPESIFIK")
    print("=" * 30)
    
    # Cek data lengkap
    data_lengkap = pd.read_excel(excel_file, sheet_name='Data_Lengkap')
    print(f"✅ Total baris data lengkap: {len(data_lengkap)}")
    print(f"✅ Kecamatan unik: {data_lengkap['Kecamatan'].nunique()}")
    print(f"✅ Bidang unik: {data_lengkap['Bidang'].nunique()}")
    print(f"✅ Total UMKM: {data_lengkap['Total'].sum():,}")
    
    # Cek pivot table
    pivot_data = pd.read_excel(excel_file, sheet_name='Per_Kecamatan_Bidang')
    print(f"✅ Pivot table berhasil dibuat dengan {len(pivot_data)} baris")
    
    # Cek ringkasan kecamatan
    ringkasan_kec = pd.read_excel(excel_file, sheet_name='Ringkasan_Kecamatan')
    print(f"✅ Ringkasan kecamatan: {len(ringkasan_kec)} kecamatan")
    
    # Cek ringkasan bidang
    ringkasan_bidang = pd.read_excel(excel_file, sheet_name='Ringkasan_Bidang')
    print(f"✅ Ringkasan bidang: {len(ringkasan_bidang)} bidang usaha")
    
    # Cek top 10
    top_10 = pd.read_excel(excel_file, sheet_name='Top_10_Kombinasi')
    print(f"✅ Top 10 kombinasi: {len(top_10)} entri")
    
    print(f"\n🎉 SEMUA VERIFIKASI BERHASIL!")
    print(f"📁 File '{excel_file}' siap digunakan untuk analisis")
    
except Exception as e:
    print(f"❌ Error dalam verifikasi: {e}")
