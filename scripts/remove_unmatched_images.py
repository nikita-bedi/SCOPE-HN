#!/usr/bin/env python3
"""
Remove images that don't have corresponding masks to achieve perfect 942/942 match.
This script will remove:
- Patient 014: SCOPE_HN_014_2 (any extension)
- Patient 022: SCOPE_HN_022_7 (any extension)
"""

import subprocess
import sys

def run_rclone_command(command, dry_run=False):
    """Run rclone command and return output."""
    if dry_run:
        print(f"DRY RUN: {command}")
        return True
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        print(f"SUCCESS: {command}")
        if result.stdout:
            print(f"Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {command}")
        print(f"Error: {e.stderr}")
        return False

def list_files_in_directory(patient_id):
    """List all files in a patient's images directory."""
    command = f"rclone lsf gdrive:/Rau_So_Segmentation_Dataset/SCOPE_HN/{patient_id}/images/"
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return [f.strip() for f in result.stdout.strip().split('\n') if f.strip()]
    except subprocess.CalledProcessError as e:
        print(f"Error listing files for patient {patient_id}: {e.stderr}")
        return []

def find_and_remove_image(patient_id, base_name, dry_run=False):
    """Find and remove an image with the given base name."""
    print(f"\n=== Processing Patient {patient_id}: {base_name} ===")
    
    # List all files in the patient's images directory
    files = list_files_in_directory(patient_id)
    
    # Find files that match the base name
    matching_files = [f for f in files if f.startswith(base_name + '.') or f == base_name]
    
    if not matching_files:
        print(f"No files found matching '{base_name}' for patient {patient_id}")
        return False
    
    print(f"Found {len(matching_files)} matching file(s): {matching_files}")
    
    # Remove each matching file
    success = True
    for filename in matching_files:
        file_path = f"gdrive:/Rau_So_Segmentation_Dataset/SCOPE_HN/{patient_id}/images/{filename}"
        command = f"rclone delete '{file_path}'"
        
        if not run_rclone_command(command, dry_run):
            success = False
    
    return success

def main():
    print("=== SCOPE-HN Dataset: Remove Unmatched Images ===\n")
    
    # Images to remove (identified from discrepancy analysis)
    images_to_remove = [
        ("014", "SCOPE_HN_014_2"),
        ("022", "SCOPE_HN_022_7")
    ]
    
    # Check if user wants to do a dry run first
    if len(sys.argv) > 1 and sys.argv[1] == "--dry-run":
        print("DRY RUN MODE - No files will actually be deleted\n")
        dry_run = True
    else:
        print("LIVE MODE - Files will be permanently deleted")
        response = input("Are you sure you want to proceed? (yes/no): ")
        if response.lower() != 'yes':
            print("Operation cancelled.")
            return
        dry_run = False
    
    print("\n" + "="*50)
    
    # Process each image
    total_success = True
    for patient_id, base_name in images_to_remove:
        success = find_and_remove_image(patient_id, base_name, dry_run)
        if not success:
            total_success = False
    
    print("\n" + "="*50)
    
    if total_success:
        print("✅ All operations completed successfully!")
        if not dry_run:
            print("Dataset now has perfect 942/942 image-mask pairs.")
    else:
        print("❌ Some operations failed. Please check the errors above.")
    
    print("\nTo verify the cleanup, run the discrepancy analysis script again:")
    print("python3 find_image_mask_discrepancy.py")

if __name__ == "__main__":
    main()
