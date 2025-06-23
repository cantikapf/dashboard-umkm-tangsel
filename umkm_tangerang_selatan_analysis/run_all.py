"""
🚀 Run All - One-click Automation Script
Orchestrates the entire UMKM analysis and dashboard process
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from umkm_data_processor import UMKMDataProcessor
from dashboard_umkm import UMKMDashboard

def setup_environment():
    """Set up the project environment"""
    print("\n🔧 SETTING UP ENVIRONMENT")
    print("=" * 50)
    
    # Define paths
    root_dir = Path(__file__).parent
    data_dir = root_dir / 'data'
    output_dir = root_dir / 'data_output'
    
    # Create directories if they don't exist
    data_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)
    
    # Copy CSV files from source directory if needed
    source_dir = root_dir.parent / 'Data'
    if source_dir.exists():
        print("📂 Copying CSV files from source directory...")
        for file in source_dir.glob('*.csv'):
            if not file.name.startswith('~'):  # Skip temporary files
                shutil.copy2(file, data_dir / file.name)
                print(f"   ✅ Copied: {file.name}")
    
    return data_dir, output_dir

def process_data(data_dir, output_dir):
    """Process UMKM data"""
    print("\n🔄 PROCESSING UMKM DATA")
    print("=" * 50)
    
    processor = UMKMDataProcessor(
        data_folder=str(data_dir),
        output_folder=str(output_dir)
    )
    
    success = False
    if processor.load_csv_files():
        if processor.process_data():
            # Save both Excel and JSON outputs
            processor.save_excel_analysis()
            processor.save_json_data()
            processor.print_summary()
            success = True
    
    return success

def launch_dashboard(port=8050):
    """Launch the interactive dashboard"""
    print("\n🚀 LAUNCHING DASHBOARD")
    print("=" * 50)
    print(f"Dashboard will be available at: http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    
    dashboard = UMKMDashboard()
    dashboard.run_server(port=port)

def main():
    """Main execution function"""
    print("\n🎯 UMKM TANGERANG SELATAN ANALYSIS")
    print("=" * 50)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Step 1: Setup
        data_dir, output_dir = setup_environment()
        
        # Step 2: Process Data
        if process_data(data_dir, output_dir):
            # Step 3: Launch Dashboard
            launch_dashboard()
        else:
            print("\n❌ Data processing failed. Dashboard cannot be launched.")
            
    except KeyboardInterrupt:
        print("\n\n👋 Dashboard stopped by user")
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
    finally:
        print(f"\n✨ Process completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
