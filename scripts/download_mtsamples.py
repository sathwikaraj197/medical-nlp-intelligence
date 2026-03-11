
import os
import requests
from pathlib import Path
import json
import time

class MTSamplesDownloader:
    """
    Download medical transcription samples from MTSamples
    """
    
    def __init__(self, output_dir="data/raw/mtsamples"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # MTSamples API endpoint (using Kaggle dataset mirror)
        self.dataset_url = "https://raw.githubusercontent.com/satyaborg/mtsamples/master/mtsamples.csv"
        
    def download_dataset(self):
        """
        Download MTSamples dataset from GitHub mirror
        """
        print("📥 Downloading MTSamples dataset...")
        print(f"   Source: {self.dataset_url}")
        print(f"   Destination: {self.output_dir}")
        
        try:
            # Download CSV file
            response = requests.get(self.dataset_url, timeout=30)
            response.raise_for_status()
            
            # Save to file
            csv_path = self.output_dir / "mtsamples.csv"
            with open(csv_path, 'wb') as f:
                f.write(response.content)
            
            print(f"\n✅ Dataset downloaded successfully!")
            print(f"   Saved to: {csv_path}")
            
            return csv_path
            
        except Exception as e:
            print(f"\n❌ Error downloading dataset: {e}")
            print("\nAlternative: Download manually from:")
            print("   https://www.kaggle.com/datasets/tboyle10/medicaltranscriptions")
            return None
    
    def process_dataset(self, csv_path):
        """
        Process CSV and convert to individual text files
        """
        import pandas as pd
        
        print("\n🔄 Processing dataset...")
        
        try:
            # Read CSV
            df = pd.read_csv(csv_path)
            
            print(f"   Total samples: {len(df)}")
            print(f"   Columns: {list(df.columns)}")
            
            # Create output directory for text files
            text_dir = self.output_dir / "texts"
            text_dir.mkdir(exist_ok=True)
            
            # Process each sample
            processed = 0
            for idx, row in df.iterrows():
                try:
                    # Combine relevant fields
                    medical_specialty = row.get('medical_specialty', 'Unknown')
                    description = row.get('description', '')
                    transcription = row.get('transcription', '')
                    
                    # Skip if no transcription
                    if pd.isna(transcription) or len(str(transcription).strip()) < 50:
                        continue
                    
                    # Create formatted text
                    content = f"""MEDICAL SPECIALTY: {medical_specialty}
DESCRIPTION: {description}

TRANSCRIPTION:
{transcription}
"""
                    
                    # Save to file
                    filename = f"sample_{idx:04d}_{medical_specialty.replace(' ', '_').replace('/', '-')}.txt"
                    filepath = text_dir / filename
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    processed += 1
                    
                    if processed % 500 == 0:
                        print(f"   Processed {processed} samples...")
                
                except Exception as e:
                    print(f"   Error processing sample {idx}: {e}")
                    continue
            
            print(f"\n✅ Processed {processed} medical transcriptions")
            print(f"   Saved to: {text_dir}")
            
            # Create summary
            self._create_summary(df, text_dir, processed)
            
            return text_dir
            
        except Exception as e:
            print(f"\n❌ Error processing dataset: {e}")
            return None
    
    def _create_summary(self, df, text_dir, processed_count):
        """Create a summary of the dataset"""
        
        summary = {
            "total_samples": len(df),
            "processed_samples": processed_count,
            "specialties": df['medical_specialty'].value_counts().to_dict() if 'medical_specialty' in df.columns else {},
            "download_date": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        summary_path = text_dir / "dataset_summary.json"
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n📊 Dataset Summary:")
        print(f"   Total samples: {summary['total_samples']}")
        print(f"   Successfully processed: {summary['processed_samples']}")
        print(f"\n   Top 5 specialties:")
        
        sorted_specialties = sorted(summary['specialties'].items(), key=lambda x: x[1], reverse=True)[:5]
        for specialty, count in sorted_specialties:
            print(f"      - {specialty}: {count} samples")
    
    def download_and_process(self):
        """Complete pipeline: download and process"""
        
        # Check if already downloaded
        csv_path = self.output_dir / "mtsamples.csv"
        
        if csv_path.exists():
            print("ℹ️  Dataset already downloaded!")
            print(f"   Location: {csv_path}")
            user_input = input("\n   Re-download? (y/n): ")
            if user_input.lower() != 'y':
                print("   Using existing dataset...")
            else:
                csv_path = self.download_dataset()
        else:
            csv_path = self.download_dataset()
        
        if csv_path and csv_path.exists():
            text_dir = self.process_dataset(csv_path)
            
            if text_dir:
                print("\n" + "="*60)
                print("✅ DATASET READY!")
                print("="*60)
                print(f"Location: {text_dir}")
                print(f"\nYou can now use these files for:")
                print("  - Text preprocessing")
                print("  - Entity extraction")
                print("  - Model training")
                print("  - Testing your NLP pipeline")
                return text_dir
        
        return None


def main():
    """Main function"""
    print("="*60)
    print("MTSamples Medical Dataset Downloader")
    print("="*60)
    print()
    
    downloader = MTSamplesDownloader()
    downloader.download_and_process()
    
    print("\n✅ Done!")


if __name__ == "__main__":
    main()
