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
1. **Semantic Segmentation**: Pixel-level classification of anatomical structures
2. **Tumor Detection and Classification**: Identification and characterization of malignant tissue
3. **Anatomical Structure Recognition**: Automated identification of normal head and neck anatomy
4. **Artifact Detection**: Recognition and handling of endoscopic imaging artifacts
5. **Multi-class Classification**: Frame-level classification tasks
6. **Temporal Analysis**: Video-based progression and motion analysis

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
- **Age Group**: 18+
- **Sex**: Male/Female
- **Race/Ethnicity**: Self-reported categories (when available)

### Clinical Characteristics
- **Primary Tumor Site**: Anatomical location of primary tumor
  - Base of tongue
  - Tonsil/tonsillar pillar
  - Soft palate
  - Pharyngeal wall
  - Other oropharyngeal subsites
- **TNM Staging**: Tumor classification

## Licensing Terms and Data Use Conditions
STANFORD UNIVERSITY SCHOOL OF MEDICINE DATASET RESEARCH USE AGREEMENT
By registering for downloads from this Dataset, you are agreeing to this Research Use Agreement, as well as to the Terms of Use of the Stanford University School of Medicine website as posted and updated periodically at[http://www.stanford.edu/site/terms/].
1. Permission is granted to view and use the Dataset without charge for personal, non-commercial research purposes only. Any commercial use, sale, or other monetization is prohibited.
2. Other than the rights granted herein, the Stanford University School of Medicine (ÒSchool of MedicineÓ) retains all rights, title, and interest in the Dataset.
3. You may make a verbatim copy of the Dataset for personal, non-commercial research use as permitted in this Research Use Agreement. If another user within your organization wishes to use the Dataset, they must register as an individual user and comply with all the terms of this Research Use Agreement.
4. YOU MAY NOT DISTRIBUTE, PUBLISH, OR REPRODUCE A COPY of any portion or all of the Dataset to others without specific prior written permission from the School of Medicine.
5. YOU MAY NOT SHARE THE DOWNLOAD LINK to the dataset to others. If another user within your organization wishes to use the Dataset, they must register as an individual user and comply with all the terms of this Research Use Agreement.
6. You must not modify, reverse engineer, decompile, or create derivative works from the Dataset. You must not remove or alter any copyright or other proprietary notices in the Dataset.
7. The Dataset has not been reviewed or approved by the Food and Drug Administration, and is for non-clinical, Research Use Only. In no event shall data or images generated through the use of the Dataset be used or relied upon in the diagnosis or provision of patient care.
8. THE DATASET IS PROVIDED "AS IS," AND STANFORD UNIVERSITY AND ITS COLLABORATORS DO NOT MAKE ANY WARRANTY, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE, NOR DO THEY ASSUME ANY LIABILITY OR RESPONSIBILITY FOR THE USE OF THIS DATASET.
9. You will not make any attempt to re-identify any of the individual data subjects. Re-identification of individuals is strictly prohibited. Any re-identification of any individual data subject shall be immediately reported to the School of Medicine.
10. Any violation of this Research Use Agreement or other impermissible use shall be grounds for immediate termination of use of this Dataset. In the event that the School of Medicine determines that the recipient has violated this Research Use Agreement or other impermissible use has been made, the School of Medicine may direct that the undersigned data recipient immediately return all copies of the Dataset and retain no copies thereof even if you did not cause the violation or impermissible use.
In consideration for your agreement to the terms and conditions contained here, Stanford grants you permission to view and use the Dataset for personal, non-commercial research. You may not otherwise copy, reproduce, retransmit, distribute, publish, commercially exploit or otherwise transfer any material.
**Limitation of Use**:ÊYou may use Dataset for legal purposes only.
You agree to indemnify and hold Stanford harmless from any claims, losses or damages, including legal fees, arising out of or resulting from your use of the Dataset or your violation or role in violation of these Terms. You agree to fully cooperate in StanfordÕs defense against any such claims. These Terms shall be governed by and interpreted in accordance with the laws of California.
### Ethical Considerations
- All patient data has been de-identified according to HIPAA Safe Harbor provisions
- Stanford University IRB approval was obtained for dataset creation and distribution

### Access and Distribution
The final, de-identified SCOPE-HN dataset will be available through the [Stanford AIMI platform](link) under a **CC-BY-NC 4.0** license. Raw clinical data used in these scripts is not publicly accessible.


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

**Version**: 2.0  
**Last Updated**: July 2025  
**Total Videos**: 104  
**Total Images**: 942  
**Total Annotations**: 942  
**Total Patients**: 106
