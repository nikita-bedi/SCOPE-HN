#!/usr/bin/env python3
"""
Finalize Videos Script

This script:
1. Renames all trimmed videos from 'trimmed_SCOPE_HN_xxx.mp4' to 'SCOPE_HN_xxx.mp4'
2. Copies them to a final directory
3. Uploads them to Google Drive in a 'Final Videos' folder
"""

import os
import shutil
import subprocess
import glob
from pathlib import Path

def main():
    # Directories
    trimmed_dir = "Project/trimmed_videos"
    final_dir = "Project/final_videos"
    
    print("="*60)
    print("Video Finalization Script")
    print("="*60)
    
    # Create final directory
    os.makedirs(final_dir, exist_ok=True)
    
    # Get all trimmed videos
    trimmed_videos = sorted(glob.glob(os.path.join(trimmed_dir, "trimmed_*.mp4")))
    
    if not trimmed_videos:
        print("No trimmed videos found!")
        return
    
    print(f"Found {len(trimmed_videos)} trimmed videos to process")
    print()
    
    # Process each video
    renamed_count = 0
    total_size = 0
    
    for trimmed_path in trimmed_videos:
        # Extract original filename
        filename = os.path.basename(trimmed_path)
        original_name = filename.replace("trimmed_", "")
        
        # Create final path
        final_path = os.path.join(final_dir, original_name)
        
        # Copy and rename
        try:
            shutil.copy2(trimmed_path, final_path)
            file_size = os.path.getsize(final_path)
            total_size += file_size
            renamed_count += 1
            
            print(f"✅ {filename} → {original_name} ({file_size / (1024*1024):.1f} MB)")
            
        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")
    
    print()
    print(f"✅ Successfully processed {renamed_count} videos")
    print(f"📊 Total size: {total_size / (1024*1024*1024):.2f} GB")
    print(f"📁 Final videos saved to: {final_dir}")
    print()
    
    # Upload to Google Drive
    print("🚀 Starting upload to Google Drive...")
    print("Destination: gdrive:/Rau_So_Segmentation_Dataset/Final Videos/")
    print()
    
    try:
        # Create the Final Videos folder and upload
        cmd = [
            'rclone', 'copy', final_dir + '/',
            'gdrive:/Rau_So_Segmentation_Dataset/Final Videos/',
            '--progress',
            '--transfers', '4',
            '--checkers', '8'
        ]
        
        result = subprocess.run(cmd, check=True)
        
        if result.returncode == 0:
            print("✅ Upload completed successfully!")
        else:
            print("❌ Upload failed")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Upload error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    print()
    print("="*60)
    print("FINALIZATION COMPLETE!")
    print("="*60)
    print(f"📁 Local final videos: {final_dir}")
    print(f"☁️  Google Drive: gdrive:/Rau_So_Segmentation_Dataset/Final Videos/")
    print(f"📊 Total videos: {renamed_count}")
    print(f"💾 Total size: {total_size / (1024*1024*1024):.2f} GB")

if __name__ == "__main__":
    main()
