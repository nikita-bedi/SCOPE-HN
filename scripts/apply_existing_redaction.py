#!/usr/bin/env python3
"""
Apply PHI redaction to videos using existing coordinate files.
"""

import os
import json
import subprocess
import glob
from pathlib import Path

def load_coordinate_files(coords_dir):
    """Load all coordinate files and create mapping."""
    coordinates = {}
    
    coord_files = glob.glob(os.path.join(coords_dir, "*_phi_coords.json"))
    
    for coord_file in coord_files:
        try:
            with open(coord_file, 'r') as f:
                data = json.load(f)
            
            # Extract number from filename (e.g., "001" from "001_phi_coords.json")
            filename = os.path.basename(coord_file)
            number = filename.split('_')[0]
            
            # Get coordinates
            coords = data.get('coordinates', [])
            if len(coords) == 4:
                # Convert from [x1, y1, x2, y2] to [x, y, width, height]
                x1, y1, x2, y2 = coords
                x = min(x1, x2)
                y = min(y1, y2)
                width = abs(x2 - x1)
                height = abs(y2 - y1)
                
                coordinates[number] = {
                    'x': x,
                    'y': y,
                    'width': width,
                    'height': height,
                    'original_coords': coords,
                    'folder': data.get('folder', number)
                }
                
                print(f"Loaded coordinates for {number}: x={x}, y={y}, w={width}, h={height}")
            else:
                print(f"Warning: Invalid coordinates in {coord_file}")
                
        except Exception as e:
            print(f"Error loading {coord_file}: {e}")
    
    return coordinates

def find_matching_video(number, video_dir):
    """Find the video file that matches the coordinate number."""
    # Try different patterns to match the number to video filename
    patterns = [
        f"SCOPE_HN_{number}.mp4",
        f"SCOPE_HN_{int(number):03d}.mp4",  # Convert to int and back to remove leading zeros
        f"*{number}.mp4",
        f"*{int(number):03d}.mp4"
    ]
    
    for pattern in patterns:
        matches = glob.glob(os.path.join(video_dir, pattern))
        if matches:
            return matches[0]
    
    return None

def apply_redaction_to_video(video_path, output_path, bbox_coords):
    """Apply redaction (black box) to video using ffmpeg."""
    x = bbox_coords['x']
    y = bbox_coords['y']
    width = bbox_coords['width']
    height = bbox_coords['height']
    
    # FFmpeg command to draw black rectangle over specified area
    cmd = [
        'ffmpeg', '-y', '-i', video_path,
        '-vf', f'drawbox=x={x}:y={y}:w={width}:h={height}:color=black:t=fill',
        '-c:a', 'copy',  # Copy audio if present
        '-c:v', 'libx264',  # Re-encode video with H.264
        '-preset', 'medium',  # Balance between speed and compression
        '-crf', '23',  # Good quality setting
        output_path
    ]
    
    try:
        print(f"  Processing: {os.path.basename(video_path)}")
        print(f"  Redaction box: x={x}, y={y}, w={width}, h={height}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"  ✓ Completed: {os.path.basename(output_path)}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Error processing {video_path}: {e}")
        if e.stderr:
            print(f"  Error details: {e.stderr[:200]}...")
        return False

def main():
    # Configuration
    video_dir = "rau_so_seg_videos_noaudio"
    coords_dir = os.path.join(video_dir, "phi_coords")
    output_dir = "rau_so_seg_videos_redacted"
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    print("PHI Redaction Processor")
    print("=" * 50)
    print(f"Video directory: {video_dir}")
    print(f"Coordinates directory: {coords_dir}")
    print(f"Output directory: {output_dir}")
    
    # Load coordinate files
    print(f"\nLoading coordinate files from {coords_dir}...")
    coordinates = load_coordinate_files(coords_dir)
    
    if not coordinates:
        print("No coordinate files found!")
        return
    
    print(f"Loaded {len(coordinates)} coordinate files")
    
    # Process each coordinate file
    print(f"\nMatching coordinates to videos...")
    matched_videos = {}
    unmatched_coords = []
    
    for number, coords in coordinates.items():
        video_path = find_matching_video(number, video_dir)
        if video_path:
            matched_videos[video_path] = coords
            print(f"✓ {number} -> {os.path.basename(video_path)}")
        else:
            unmatched_coords.append(number)
            print(f"✗ {number} -> No matching video found")
    
    print(f"\nMatched: {len(matched_videos)} videos")
    if unmatched_coords:
        print(f"Unmatched coordinates: {unmatched_coords}")
    
    if not matched_videos:
        print("No videos matched with coordinates!")
        return
    
    # Apply redaction to matched videos
    print(f"\nApplying redaction to {len(matched_videos)} videos...")
    print("-" * 50)
    
    success_count = 0
    total_count = len(matched_videos)
    
    for video_path, coords in matched_videos.items():
        video_name = os.path.basename(video_path)
        output_path = os.path.join(output_dir, video_name)
        
        if apply_redaction_to_video(video_path, output_path, coords):
            success_count += 1
    
    print("-" * 50)
    print(f"Redaction complete: {success_count}/{total_count} videos processed successfully")
    
    if success_count > 0:
        print(f"Redacted videos saved to: {output_dir}/")
        
        # Show sample of what was processed
        print(f"\nSample of processed videos:")
        for i, (video_path, coords) in enumerate(list(matched_videos.items())[:5]):
            video_name = os.path.basename(video_path)
            print(f"  {video_name}: redacted area {coords['width']}x{coords['height']} at ({coords['x']}, {coords['y']})")
        
        if len(matched_videos) > 5:
            print(f"  ... and {len(matched_videos) - 5} more videos")

if __name__ == "__main__":
    main()
