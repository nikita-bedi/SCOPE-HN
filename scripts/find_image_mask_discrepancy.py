#!/usr/bin/env python3
"""
Find discrepancies between images and masks in SCOPE_HN dataset on Google Drive.
This script identifies:
1. Images without corresponding masks
2. Masks without corresponding images
3. Summary statistics
"""

import subprocess
import json
import os
from pathlib import Path
import re

def run_rclone_command(command):
    """Run rclone command and return output."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip().split('\n') if result.stdout.strip() else []
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error: {e.stderr}")
        return []

def get_patient_directories():
    """Get all patient directories."""
    command = "rclone lsf gdrive:/Rau_So_Segmentation_Dataset/SCOPE_HN/ --dirs-only"
    return [d.rstrip('/') for d in run_rclone_command(command) if d.strip()]

def get_patient_images(patient_id):
    """Get all image files for a specific patient."""
    command = f"rclone lsf gdrive:/Rau_So_Segmentation_Dataset/SCOPE_HN/{patient_id}/images/"
    files = run_rclone_command(command)
    return [f for f in files if f.strip()]

def get_patient_masks(patient_id):
    """Get all mask files for a specific patient."""
    command = f"rclone lsf gdrive:/Rau_So_Segmentation_Dataset/SCOPE_HN/{patient_id}/masks/"
    files = run_rclone_command(command)
    return [f for f in files if f.strip()]

def find_discrepancies_by_patient(patient_id):
    """Find discrepancies for a specific patient."""
    images = get_patient_images(patient_id)
    masks = get_patient_masks(patient_id)
    
    # Create base name sets (without extensions)
    image_bases = {Path(f).stem for f in images}
    mask_bases = {Path(f).stem for f in masks}
    
    # Find discrepancies
    images_without_masks = image_bases - mask_bases
    masks_without_images = mask_bases - image_bases
    matching_pairs = image_bases & mask_bases
    
    return {
        'images': images,
        'masks': masks,
        'image_bases': image_bases,
        'mask_bases': mask_bases,
        'images_without_masks': images_without_masks,
        'masks_without_images': masks_without_images,
        'matching_pairs': matching_pairs,
        'total_images': len(images),
        'total_masks': len(masks),
        'total_matches': len(matching_pairs)
    }

def analyze_by_patient(images, masks):
    """Analyze discrepancies by patient."""
    patient_stats = {}
    
    # Get all patient IDs
    all_patients = set()
    for key in images.keys():
        patient_id = key.split('/')[0]
        all_patients.add(patient_id)
    for key in masks.keys():
        patient_id = key.split('/')[0]
        all_patients.add(patient_id)
    
    for patient_id in sorted(all_patients):
        patient_images = {k: v for k, v in images.items() if k.startswith(f"{patient_id}/")}
        patient_masks = {k: v for k, v in masks.items() if k.startswith(f"{patient_id}/")}
        
        patient_stats[patient_id] = {
            'images': len(patient_images),
            'masks': len(patient_masks),
            'difference': len(patient_images) - len(patient_masks)
        }
    
    return patient_stats

def main():
    print("=== SCOPE-HN Dataset: Image-Mask Discrepancy Analysis ===\n")
    
    # Get all patient directories
    patients = get_patient_directories()
    print(f"Found {len(patients)} patient directories\n")
    
    total_images = 0
    total_masks = 0
    total_matches = 0
    patients_with_discrepancies = []
    all_images_without_masks = []
    all_masks_without_images = []
    
    print("=== PATIENT-WISE ANALYSIS ===")
    for patient_id in sorted(patients):
        try:
            analysis = find_discrepancies_by_patient(patient_id)
            
            total_images += analysis['total_images']
            total_masks += analysis['total_masks']
            total_matches += analysis['total_matches']
            
            # Check for discrepancies
            if analysis['images_without_masks'] or analysis['masks_without_images']:
                patients_with_discrepancies.append(patient_id)
                print(f"Patient {patient_id}: {analysis['total_images']} images, {analysis['total_masks']} masks - DISCREPANCY FOUND")
                
                if analysis['images_without_masks']:
                    for img in analysis['images_without_masks']:
                        all_images_without_masks.append(f"Patient {patient_id}: {img}")
                        
                if analysis['masks_without_images']:
                    for mask in analysis['masks_without_images']:
                        all_masks_without_images.append(f"Patient {patient_id}: {mask}")
            elif analysis['total_images'] != analysis['total_masks']:
                patients_with_discrepancies.append(patient_id)
                diff = analysis['total_images'] - analysis['total_masks']
                print(f"Patient {patient_id}: {analysis['total_images']} images, {analysis['total_masks']} masks (diff: {diff:+d})")
            else:
                print(f"Patient {patient_id}: {analysis['total_images']} images, {analysis['total_masks']} masks - PERFECT MATCH")
                
        except Exception as e:
            print(f"Patient {patient_id}: ERROR - {e}")
    
    print("\n=== SUMMARY ===")
    print(f"Total images found: {total_images}")
    print(f"Total masks found: {total_masks}")
    print(f"Total matching pairs: {total_matches}")
    print(f"Images without masks: {len(all_images_without_masks)}")
    print(f"Masks without images: {len(all_masks_without_images)}")
    
    if all_images_without_masks:
        print("\n=== IMAGES WITHOUT MASKS ===")
        for item in all_images_without_masks:
            print(item)
    
    if all_masks_without_images:
        print("\n=== MASKS WITHOUT IMAGES ===")
        for item in all_masks_without_images:
            print(item)
    
    print("\n=== STATISTICS ===")
    print(f"Total patients analyzed: {len(patients)}")
    print(f"Patients with discrepancies: {len(patients_with_discrepancies)}")
    print(f"Patients with perfect matches: {len(patients) - len(patients_with_discrepancies)}")

if __name__ == "__main__":
    main()
