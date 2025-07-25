# SCOPE-HN Dataset Setup Guide

This guide will help you set up the environment and tools needed to work with the SCOPE-HN dataset and its processing scripts.

## Prerequisites

- Python 3.7 or higher
- Git (for cloning the repository)
- Internet connection (for downloading dependencies and accessing Google Drive)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/[your-username]/SCOPE-HN-Dataset.git
cd SCOPE-HN-Dataset
```

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv scope_hn_env

# Activate virtual environment
# On Linux/macOS:
source scope_hn_env/bin/activate
# On Windows:
scope_hn_env\Scripts\activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install External Tools

#### rclone (Required for Google Drive access)

**Linux/macOS:**
```bash
curl https://rclone.org/install.sh | sudo bash
```

**Windows:**
1. Download from [https://rclone.org/downloads/](https://rclone.org/downloads/)
2. Extract and add to PATH

#### FFmpeg (Required for video processing)

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
1. Download from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Extract and add to PATH

### 5. Configure Google Drive Access

```bash
rclone config
```

Follow the interactive prompts:
1. Choose "n" for new remote
2. Name it "gdrive"
3. Choose "drive" for Google Drive
4. Follow authentication steps
5. Choose "1" for full access

## Dataset Access

The SCOPE-HN dataset is hosted on Google Drive and accessed through the Stanford AIMI platform. To access the dataset:

1. **Request Access**: Visit [Stanford AIMI platform](https://aimi.stanford.edu)
2. **Complete Data Use Agreement**: Sign the required agreements
3. **Receive Access Credentials**: You'll receive Google Drive access
4. **Configure rclone**: Use the provided credentials with rclone

## Verification

Test your setup:

```bash
# Test Python dependencies
python -c "import numpy, cv2, matplotlib, PIL; print('Python dependencies OK')"

# Test rclone configuration
rclone lsd gdrive:

# Test FFmpeg
ffmpeg -version
```

## Directory Structure

After setup, your project should look like:

```
SCOPE-HN-Dataset/
├── README.md                 # Main dataset documentation
├── SETUP.md                 # This setup guide
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules
├── scripts/                # Processing scripts
│   ├── README.md           # Scripts documentation
│   ├── interactive_redaction.py
│   ├── web_video_trimmer.py
│   ├── apply_existing_redaction.py
│   ├── finalize_videos.py
│   ├── find_image_mask_discrepancy.py
│   └── remove_unmatched_images.py
├── docs/                   # Additional documentation
├── tools/                  # Utility tools
└── examples/              # Usage examples
```

## Quick Start

1. **Validate Dataset Integrity**:
   ```bash
   cd scripts
   python find_image_mask_discrepancy.py
   ```

2. **Start Video Trimming Interface**:
   ```bash
   python web_video_trimmer.py
   # Open browser to http://localhost:8080
   ```

3. **Interactive PHI Redaction**:
   ```bash
   python interactive_redaction.py
   ```

## Troubleshooting

### Common Issues

**"rclone not found"**
- Ensure rclone is installed and in your PATH
- Try `which rclone` (Linux/macOS) or `where rclone` (Windows)

**"Permission denied" errors**
- Check file permissions: `chmod +x scripts/*.py`
- Ensure you have write access to the working directory

**"Module not found" errors**
- Activate your virtual environment
- Reinstall requirements: `pip install -r requirements.txt`

**Google Drive access issues**
- Reconfigure rclone: `rclone config`
- Test connection: `rclone lsd gdrive:`
- Check data use agreement status

### Performance Tips

- Use SSD storage for video processing
- Ensure sufficient RAM (8GB+ recommended)
- Close unnecessary applications during processing
- Use batch processing for large datasets

## Support

For technical support:
- Check the [scripts documentation](scripts/README.md)
- Review the main [README.md](README.md)
- Contact the dataset maintainers (see README.md for contact info)

## Security Notes

- Never commit credentials to version control
- Use virtual environments to isolate dependencies
- Regularly update dependencies for security patches
- Follow your institution's data handling policies

## License

This setup and the associated scripts are released under the same license as the SCOPE-HN dataset. See the main README.md for licensing details.
