#!/usr/bin/env python3
"""
SCOPE-HN Dataset Validation Example

This example demonstrates how to validate the SCOPE-HN dataset integrity
and generate a summary report of the dataset statistics.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from find_image_mask_discrepancy import *

def generate_dataset_summary():
    """Generate a comprehensive summary of the SCOPE-HN dataset."""
    print("=" * 60)
    print("SCOPE-HN DATASET VALIDATION AND SUMMARY")
    print("=" * 60)
    
    # Get all patient directories
    patients = get_patient_directories()
    print(f"📊 Found {len(patients)} patient directories")
    
    total_images = 0
    total_masks = 0
    total_matches = 0
    patients_with_issues = []
    patient_stats = []
    
    print("\n🔍 Analyzing each patient...")
    for patient_id in sorted(patients):
        try:
            analysis = find_discrepancies_by_patient(patient_id)
            
            total_images += analysis['total_images']
            total_masks += analysis['total_masks']
            total_matches += analysis['total_matches']
            
            patient_stats.append({
                'id': patient_id,
                'images': analysis['total_images'],
                'masks': analysis['total_masks'],
                'matches': analysis['total_matches'],
                'perfect': analysis['total_images'] == analysis['total_masks'] == analysis['total_matches']
            })
            
            if not (analysis['total_images'] == analysis['total_masks'] == analysis['total_matches']):
                patients_with_issues.append(patient_id)
                
        except Exception as e:
            print(f"❌ Error analyzing patient {patient_id}: {e}")
            patients_with_issues.append(patient_id)
    
    # Generate summary statistics
    print("\n" + "=" * 60)
    print("DATASET SUMMARY")
    print("=" * 60)
    
    print(f"📈 Total Statistics:")
    print(f"   • Patients: {len(patients)}")
    print(f"   • Images: {total_images}")
    print(f"   • Masks: {total_masks}")
    print(f"   • Perfect Matches: {total_matches}")
    
    print(f"\n✅ Quality Metrics:")
    perfect_patients = len(patients) - len(patients_with_issues)
    print(f"   • Patients with perfect matches: {perfect_patients}/{len(patients)} ({perfect_patients/len(patients)*100:.1f}%)")
    print(f"   • Overall completion rate: {total_matches/total_images*100:.1f}%")
    
    if patients_with_issues:
        print(f"\n⚠️  Patients requiring attention: {len(patients_with_issues)}")
        for patient_id in patients_with_issues:
            print(f"   • Patient {patient_id}")
    else:
        print(f"\n🎉 All patients have perfect image-mask matching!")
    
    # Distribution analysis
    image_counts = [p['images'] for p in patient_stats]
    print(f"\n📊 Image Distribution:")
    print(f"   • Min images per patient: {min(image_counts)}")
    print(f"   • Max images per patient: {max(image_counts)}")
    print(f"   • Average images per patient: {sum(image_counts)/len(image_counts):.1f}")
    
    return {
        'total_patients': len(patients),
        'total_images': total_images,
        'total_masks': total_masks,
        'total_matches': total_matches,
        'perfect_patients': perfect_patients,
        'patients_with_issues': patients_with_issues
    }

def main():
    """Main function to run the dataset validation example."""
    try:
        summary = generate_dataset_summary()
        
        print("\n" + "=" * 60)
        print("VALIDATION COMPLETE")
        print("=" * 60)
        
        if summary['patients_with_issues']:
            print("⚠️  Dataset validation completed with issues.")
            print("   Run the discrepancy analysis script for detailed information.")
            return 1
        else:
            print("✅ Dataset validation passed successfully!")
            print("   The SCOPE-HN dataset is ready for use.")
            return 0
            
    except Exception as e:
        print(f"❌ Validation failed with error: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
