# SCOPE-HN Dataset Processing Scripts

This directory contains the Python scripts used to process and curate the SCOPE-HN dataset. These scripts handle video processing, PHI redaction, frame extraction, and dataset validation.

## Scripts Overview

### 1. `interactive_redaction.py`
**Purpose**: Interactive PHI redaction tool using matplotlib for frame display and bounding box selection.

**Features**:
- Visual interface for selecting PHI regions on sample frames
- Saves redaction coordinates to JSON for batch application
- Supports navigation between multiple videos
- Real-time preview of redaction areas

**Usage**:
```bash
python interactive_redaction.py
```

**Requirements**: matplotlib, PIL, numpy

---

### 2. `web_video_trimmer.py`
**Purpose**: Web-based interface for reviewing videos and specifying time ranges to keep.

**Features**:
- Browser-based video review interface
- Batch processing with progress tracking
- Removes pre-scope and post-scope segments
- Excludes FEES (Fiberoptic Endoscopic Evaluation of Swallowing) clips
- Generates preview frames for quality assessment
- Logs all trimming operations

**Usage**:
```bash
python web_video_trimmer.py
```

**Access**: Open browser to `http://localhost:8080`

**Requirements**: Flask, ffmpeg-python, subprocess

---

### 3. `apply_existing_redaction.py`
**Purpose**: Applies previously defined redaction coordinates to all frames in videos.

**Features**:
- Batch application of redaction masks
- Consistent PHI removal across all frames
- Preserves video quality while obscuring sensitive information
- Progress tracking for large datasets

**Usage**:
```bash
python apply_existing_redaction.py
```

**Requirements**: opencv-python, numpy, json

---

### 4. `finalize_videos.py`
**Purpose**: Final video processing and quality assurance.

**Features**:
- Audio track removal for privacy compliance
- Video format standardization
- Quality validation checks
- Metadata cleanup

**Usage**:
```bash
python finalize_videos.py
```

**Requirements**: ffmpeg-python

---

### 5. `find_image_mask_discrepancy.py`
**Purpose**: Validates dataset integrity by finding discrepancies between images and annotation masks.

**Features**:
- Patient-wise analysis of image-mask pairs
- Identifies missing annotations or orphaned images
- Generates detailed discrepancy reports
- Supports Google Drive integration via rclone

**Usage**:
```bash
python find_image_mask_discrepancy.py
```

**Requirements**: subprocess, pathlib, rclone (external)

---

### 6. `remove_unmatched_images.py`
**Purpose**: Removes images that don't have corresponding annotation masks to ensure dataset consistency.

**Features**:
- Dry-run mode for safe preview
- Selective removal of unmatched images
- Maintains perfect image-mask pairing
- Detailed logging of all operations

**Usage**:
```bash
# Dry run (preview only)
python remove_unmatched_images.py --dry-run

# Execute removal
python remove_unmatched_images.py
```

**Requirements**: subprocess, rclone (external)

---

## Setup Instructions

### 1. Install Python Dependencies
```bash
pip install -r ../requirements.txt
```

### 2. Install External Dependencies

#### rclone (for Google Drive access)
```bash
# Ubuntu/Debian
curl https://rclone.org/install.sh | sudo bash

# macOS
brew install rclone

# Windows
# Download from https://rclone.org/downloads/
```

#### FFmpeg (for video processing)
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

### 3. Configure rclone for Google Drive
```bash
rclone config
# Follow prompts to set up Google Drive access
# Name the remote: "gdrive"
```

## Processing Workflow

The typical workflow for processing the SCOPE-HN dataset:

1. **Extract Sample Frames**: Use video processing tools to extract representative frames
2. **Interactive Redaction**: Run `interactive_redaction.py` to define PHI regions
3. **Video Trimming**: Use `web_video_trimmer.py` to remove non-diagnostic segments
4. **Apply Redaction**: Run `apply_existing_redaction.py` to redact all frames
5. **Finalize Videos**: Run `finalize_videos.py` for final processing
6. **Validate Dataset**: Use `find_image_mask_discrepancy.py` to check integrity
7. **Clean Dataset**: Use `remove_unmatched_images.py` if needed for perfect matching

## Data Privacy and Security

All scripts are designed with privacy and security in mind:
- PHI redaction is applied consistently across all frames
- Audio tracks are completely removed
- Temporary files are cleaned up automatically
- All operations are logged for audit purposes

## Support and Troubleshooting

For issues with these scripts:
1. Check that all dependencies are installed
2. Verify rclone configuration for Google Drive access
3. Ensure sufficient disk space for video processing
4. Check file permissions for input/output directories

## Citation

If you use these scripts in your research, please cite the SCOPE-HN dataset paper:
```
[Citation information will be provided upon publication]
```
