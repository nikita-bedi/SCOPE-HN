# SCOPE-HN Dataset

## Overview

Oropharyngeal cancer (OPC) is one of the few cancers with a rising incidence, driven primarily by increasing rates of human papillomavirus (HPV)-associated disease. Early detection and accurate delineation of OPC are critical for diagnosis, treatment planning and improving outcomes but remain challenging due to anatomical complexity and variability in clinical expertise. 

We present the SCOPE-HN dataset, a curated collection of annotated endoscopic images from 106 patients with histologically confirmed OPC, collected at Stanford between 2015 and 2023. The dataset consists of 942 RGB images extracted from diagnostic nasopharyngolaryngoscopy videos, with complete pixel-level annotations performed by expert Head and Neck surgeons. Annotations include 12 semantic classes representing tumor, normal anatomical structures, and common endoscopic artifacts. SCOPE-HN is designed to support a range of machine learning applications in endoscopic tissue segmentation, tumor classification, and clinical benchmarking.

## Dataset Structure and Naming Conventions

The SCOPE-HN dataset follows a standardized naming convention and directory structure:

### Directory Structure
```
SCOPE-HN/
├── videos/                          # Original endoscopic videos
│   ├── SCOPE_HN_001.mp4
│   ├── SCOPE_HN_002.mp4
│   └── ...
├── images/                          # Extracted frames for annotation
│   ├── SCOPE_HN_001_frame_001.jpg
│   ├── SCOPE_HN_001_frame_002.jpg
│   └── ...
├── annotations/                     # Pixel-level semantic annotations
│   ├── SCOPE_HN_001_frame_001.png
│   ├── SCOPE_HN_001_frame_002.png
│   └── ...
├── metadata/                        # Patient and clinical metadata
│   ├── patient_info.csv
│   └── annotation_metadata.json
└── README.md                        # This file
```

### Naming Conventions
- **Video files**: `SCOPE_HN_XXX.mp4` where XXX is a zero-padded patient identifier (001-126)
- **Image files**: `SCOPE_HN_XXX_frame_YYY.jpg` where XXX is the patient ID and YYY is the frame number
- **Annotation files**: `SCOPE_HN_XXX_frame_YYY.png` corresponding to each image file
- **Patient identifiers**: Sequential numbering from 001 to 126 (some numbers may be missing due to exclusion criteria)

### Data Processing Pipeline
The dataset underwent comprehensive preprocessing to ensure privacy compliance and data quality:

1. **PHI Redaction**: Manual identification and redaction of Protected Health Information (PHI)
   - Expert reviewers selected bounding boxes on sample frames to identify PHI regions
   - Redaction coordinates were applied consistently across all frames and videos
   - All patient-identifying information, timestamps, and institutional logos were obscured

2. **Video Trimming**: Manual curation to remove non-diagnostic content
   - Removal of scope insertion and withdrawal phases
   - Exclusion of Fiberoptic Endoscopic Evaluation of Swallowing (FEES) clips
   - Retention of only diagnostically relevant endoscopic examination segments

3. **Audio Removal**: All audio tracks were stripped from videos to eliminate potential PHI in verbal communications

## Included Modalities and Tasks

### Modalities
- **Video Data**: 104 endoscopic videos (MP4 format, H.264 encoding)
  - Resolution: Variable (typically 1920x1080 or 1280x720)
  - Frame rate: 30 fps
  - Duration: Variable (post-trimming, typically 30 seconds to 5 minutes)
  - Color space: RGB

- **Image Data**: 942 high-quality RGB frames extracted from videos
  - Format: JPEG or PNG
  - Resolution: Maintains original video resolution
  - Color depth: 24-bit RGB

- **Annotation Data**: Pixel-level semantic segmentation masks
  - Format: PNG (indexed color)
  - Classes: 12 semantic categories (see below)
  - Annotation tool: Custom annotation interface with expert validation

### Supported Tasks
1. **Semantic Segmentation**: Pixel-level classification of anatomical structures and pathology
2. **Tumor Detection and Classification**: Identification and characterization of malignant tissue
3. **Anatomical Structure Recognition**: Automated identification of normal head and neck anatomy
4. **Artifact Detection**: Recognition and handling of endoscopic imaging artifacts
5. **Clinical Decision Support**: Benchmarking algorithms for diagnostic assistance
6. **Multi-class Classification**: Frame-level classification tasks
7. **Temporal Analysis**: Video-based progression and motion analysis

### Semantic Classes
The annotation schema includes 12 distinct classes:
1. **Tumor**: Malignant oropharyngeal tissue
2. **Normal Mucosa**: Healthy mucosal surfaces
3. **Tongue Base**: Normal tongue base anatomy
4. **Soft Palate**: Normal soft palate structures
5. **Pharyngeal Wall**: Posterior and lateral pharyngeal walls
6. **Epiglottis**: Epiglottic structures
7. **Vocal Cords**: True and false vocal cords
8. **Arytenoids**: Arytenoid cartilages and surrounding tissue
9. **Scope Artifact**: Endoscope-related visual artifacts
10. **Reflection**: Light reflections and glare
11. **Motion Blur**: Movement-induced blur artifacts
12. **Background**: Non-anatomical background regions

## Patient Information Fields

The dataset includes de-identified clinical metadata for research purposes:

### Demographic Information
- **Age Group**: Categorized age ranges (e.g., 40-49, 50-59, 60-69, 70+)
- **Sex**: Male/Female
- **Race/Ethnicity**: Self-reported categories (when available)

### Clinical Characteristics
- **Primary Tumor Site**: Anatomical location of primary tumor
  - Base of tongue
  - Tonsil/tonsillar pillar
  - Soft palate
  - Pharyngeal wall
  - Other oropharyngeal subsites
- **HPV Status**: Human papillomavirus status (positive/negative/unknown)
- **TNM Staging**: Tumor, Node, Metastasis staging information
- **Histological Grade**: Tumor differentiation grade
- **Treatment History**: Prior treatments (surgery, radiation, chemotherapy)

## Licensing Terms and Data Use Conditions

### License
The SCOPE-HN dataset is released under the **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)** license.

### Permitted Uses
- Academic research and education
- Non-commercial algorithm development
- Clinical research (with appropriate IRB approval)
- Publication in peer-reviewed venues
- Open-source software development for research purposes

### Restrictions
- **No Commercial Use**: Dataset cannot be used for commercial purposes without explicit permission
- **No Re-identification**: Users must not attempt to re-identify patients or link data to other datasets
- **Attribution Required**: All publications and presentations must cite the original dataset paper
- **Derivative Works**: Any derivative datasets must maintain the same licensing terms

### Data Use Agreement Requirements
Users must agree to the following conditions:
1. Use data only for stated research purposes
2. Implement appropriate data security measures
3. Not redistribute raw data without permission
4. Report any suspected data quality issues
5. Acknowledge dataset creators in all publications
6. Share research findings with the broader community when possible

### Ethical Considerations
- All patient data has been de-identified according to HIPAA Safe Harbor provisions
- Stanford University IRB approval was obtained for dataset creation and distribution

### Access and Distribution
The final, de-identified SCOPE-HN dataset will be available through the [Stanford AIMI platform](https://stanfordaimi.azurewebsites.net/) under a **CC-BY-NC 4.0** license. Raw clinical data used in these scripts is not publicly accessible.

For now, reviewers can access the dataset for verification at [https://drive.google.com/drive/folders/1n723LsVhj4eUhn_OA-OO3ruQz2R_RF03?usp=sharing]


### Citation
When using this dataset, please cite:
```
Bedi et al., “SCOPE-HN: A Curated Dataset for Endoscopic Tissue Segmentation in Oropharyngeal Cancer”, MELBA (in press), 2025.
```

### Contact Information
For questions, technical support, or collaboration inquiries:
- **Principal Investigator**: [Chris Holsinger, MD]
- **Technical Contact**: [nbedi@stanford.edu]

### Acknowledgments
We acknowledge the patients who contributed their data to advance medical research, the clinical teams at Stanford Medicine, and the expert annotators who made this dataset possible.

---

**Version**: 1.0  
**Last Updated**: July 2025  
**Total Videos**: 104  
**Total Images**: 942  
**Total Annotations**: 942  
**Total Patients**: 106
