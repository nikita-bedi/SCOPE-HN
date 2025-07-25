#!/usr/bin/env python3
"""
Web-Based Video Trimming Interface for Medical Video Processing

This tool provides a web interface for reviewing videos and specifying 
time ranges to keep (removing pre-scope and post-scope segments).
"""

import os
import sys
import json
import subprocess
import csv
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import tempfile
import glob

class VideoTrimmerHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.trimmer = kwargs.pop('trimmer')
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        
        if parsed_path.path == '/':
            self.serve_main_page()
        elif parsed_path.path == '/api/videos':
            batch_num = int(query_params.get('batch', [1])[0])
            self.serve_video_list(batch_num)
        elif parsed_path.path == '/api/batch_info':
            self.serve_batch_info()
        elif parsed_path.path.startswith('/api/video/'):
            video_name = parsed_path.path.split('/')[-1]
            self.serve_video_info(video_name)
        elif parsed_path.path.startswith('/preview/'):
            self.serve_preview_frame(parsed_path.path[9:])
        else:
            self.send_error(404)
    
    def do_POST(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/trim':
            self.handle_trim_request()
        else:
            self.send_error(404)
    
    def serve_main_page(self):
        html = """
<!DOCTYPE html>
<html>
<head>
    <title>Medical Video Trimmer</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .video-card { border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }
        .video-info { background: #f5f5f5; padding: 10px; margin: 10px 0; border-radius: 3px; }
        .preview-frames { display: flex; flex-wrap: wrap; gap: 10px; margin: 10px 0; }
        .preview-frame { border: 1px solid #ccc; }
        .preview-frame img { max-width: 200px; height: auto; }
        .trim-controls { background: #e8f4f8; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .segment-input { margin: 5px 0; }
        .segment-input input { width: 60px; margin: 0 5px; }
        .button { background: #007cba; color: white; padding: 8px 16px; border: none; border-radius: 3px; cursor: pointer; }
        .button:hover { background: #005a87; }
        .button.secondary { background: #6c757d; }
        .button.danger { background: #dc3545; }
        .status { padding: 10px; margin: 10px 0; border-radius: 3px; }
        .status.success { background: #d4edda; color: #155724; }
        .status.error { background: #f8d7da; color: #721c24; }
        .status.info { background: #d1ecf1; color: #0c5460; }
        .hidden { display: none; }
    </style>
</head>
<body>
    <h1>Medical Video Trimmer</h1>
    <p><strong>Purpose:</strong> Remove video segments before scope insertion and after scope removal</p>
    
    <div id="status" class="status hidden"></div>
    
    <div id="batch-controls" class="status info">
        <h3>Batch Processing</h3>
        <p>Processing videos in batches of 5 for faster loading</p>
        <div id="batch-navigation"></div>
    </div>
    
    <div id="video-list">
        <h2>Loading videos...</h2>
    </div>

    <script>
        let videos = [];
        let currentVideo = null;
        let currentBatch = 1;
        let totalBatches = 1;
        let batchSize = 5;

        function showStatus(message, type = 'info') {
            const statusDiv = document.getElementById('status');
            statusDiv.className = `status ${type}`;
            statusDiv.textContent = message;
            statusDiv.classList.remove('hidden');
            
            if (type === 'success' || type === 'error') {
                setTimeout(() => {
                    statusDiv.classList.add('hidden');
                }, 5000);
            }
        }

        function loadBatchInfo() {
            fetch('/api/batch_info')
                .then(response => response.json())
                .then(data => {
                    totalBatches = data.total_batches;
                    renderBatchNavigation();
                    loadVideos(currentBatch);
                })
                .catch(error => {
                    showStatus('Error loading batch info: ' + error, 'error');
                });
        }

        function loadVideos(batchNum = 1) {
            currentBatch = batchNum;
            showStatus(`Loading batch ${batchNum}...`, 'info');
            
            fetch(`/api/videos?batch=${batchNum}`)
                .then(response => response.json())
                .then(data => {
                    videos = data.videos;
                    renderVideoList();
                    renderBatchNavigation();
                })
                .catch(error => {
                    showStatus('Error loading videos: ' + error, 'error');
                });
        }

        function renderBatchNavigation() {
            const nav = document.getElementById('batch-navigation');
            let navHTML = `<p>Batch ${currentBatch} of ${totalBatches} | Videos ${(currentBatch-1)*batchSize + 1}-${Math.min(currentBatch*batchSize, videos.length + (currentBatch-1)*batchSize)}</p>`;
            
            navHTML += '<div>';
            if (currentBatch > 1) {
                navHTML += `<button class="button secondary" onclick="loadVideos(${currentBatch - 1})">← Previous Batch</button> `;
            }
            
            for (let i = 1; i <= totalBatches; i++) {
                if (i === currentBatch) {
                    navHTML += `<button class="button" style="background: #28a745;">${i}</button> `;
                } else {
                    navHTML += `<button class="button secondary" onclick="loadVideos(${i})">${i}</button> `;
                }
            }
            
            if (currentBatch < totalBatches) {
                navHTML += `<button class="button secondary" onclick="loadVideos(${currentBatch + 1})">Next Batch →</button>`;
            }
            navHTML += '</div>';
            
            nav.innerHTML = navHTML;
        }

        function renderVideoList() {
            const container = document.getElementById('video-list');
            const startNum = (currentBatch - 1) * batchSize + 1;
            container.innerHTML = `<h2>Batch ${currentBatch} - Videos ${startNum} to ${startNum + videos.length - 1}</h2>`;
            
            videos.forEach((video, index) => {
                const globalIndex = (currentBatch - 1) * batchSize + index + 1;
                const card = document.createElement('div');
                card.className = 'video-card';
                card.innerHTML = `
                    <h3>#${globalIndex}: ${video.name}</h3>
                    <div class="video-info">
                        <strong>Duration:</strong> ${video.duration.toFixed(1)}s (${(video.duration/60).toFixed(1)} min)<br>
                        <strong>Size:</strong> ${video.size_mb.toFixed(1)} MB<br>
                        <strong>Resolution:</strong> ${video.width}x${video.height}
                        ${video.processed ? '<br><strong style="color: green;">✅ Already Processed</strong>' : ''}
                    </div>
                    <button class="button" onclick="reviewVideo('${video.name}')">Review & Trim</button>
                    <button class="button secondary" onclick="skipVideo('${video.name}')">Skip</button>
                `;
                container.appendChild(card);
            });
        }

        function reviewVideo(videoName) {
            showStatus('Loading video details...', 'info');
            
            fetch(`/api/video/${videoName}`)
                .then(response => response.json())
                .then(data => {
                    currentVideo = data;
                    showVideoReview(data);
                })
                .catch(error => {
                    showStatus('Error loading video details: ' + error, 'error');
                });
        }

        function showVideoReview(video) {
            const container = document.getElementById('video-list');
            container.innerHTML = `
                <button class="button secondary" onclick="loadVideos(currentBatch)">← Back to Batch ${currentBatch}</button>
                
                <h2>Review: ${video.name}</h2>
                
                <div class="video-info">
                    <strong>Duration:</strong> ${video.duration.toFixed(1)} seconds (${(video.duration/60).toFixed(1)} minutes)<br>
                    <strong>Size:</strong> ${video.size_mb.toFixed(1)} MB<br>
                    <strong>Resolution:</strong> ${video.width}x${video.height}<br>
                    <strong>Codec:</strong> ${video.codec}
                </div>

                <h3>Preview Frames</h3>
                <div class="preview-frames" id="preview-frames">
                    ${video.preview_frames.map(frame => `
                        <div class="preview-frame">
                            <img src="/preview/${frame.filename}" alt="Frame at ${frame.timestamp.toFixed(1)}s">
                            <div style="text-align: center; padding: 5px;">
                                <small>${frame.timestamp.toFixed(1)}s</small>
                            </div>
                        </div>
                    `).join('')}
                </div>

                <div class="trim-controls">
                    <h3>Specify Time Ranges to KEEP</h3>
                    <p><strong>Goal:</strong> Remove segments before scope insertion and after scope removal</p>
                    <p><strong>Video Duration:</strong> ${video.duration.toFixed(1)} seconds</p>
                    
                    <div id="segments">
                        <div class="segment-input">
                            <label>Segment 1: Keep from 
                                <input type="number" id="start1" placeholder="0" step="0.1" min="0" max="${video.duration}"> 
                                to 
                                <input type="number" id="end1" placeholder="${video.duration}" step="0.1" min="0" max="${video.duration}"> 
                                seconds
                            </label>
                        </div>
                    </div>
                    
                    <button class="button secondary" onclick="addSegment()">Add Another Segment</button>
                    <br><br>
                    
                    <button class="button" onclick="trimVideo()">Trim Video</button>
                    <button class="button secondary" onclick="skipVideo('${video.name}')">Skip This Video</button>
                </div>
            `;
        }

        let segmentCount = 1;

        function addSegment() {
            segmentCount++;
            const segmentsDiv = document.getElementById('segments');
            const newSegment = document.createElement('div');
            newSegment.className = 'segment-input';
            newSegment.innerHTML = `
                <label>Segment ${segmentCount}: Keep from 
                    <input type="number" id="start${segmentCount}" placeholder="0" step="0.1" min="0" max="${currentVideo.duration}"> 
                    to 
                    <input type="number" id="end${segmentCount}" placeholder="${currentVideo.duration}" step="0.1" min="0" max="${currentVideo.duration}"> 
                    seconds
                </label>
            `;
            segmentsDiv.appendChild(newSegment);
        }

        function trimVideo() {
            if (!currentVideo) return;

            // Collect segments
            const segments = [];
            for (let i = 1; i <= segmentCount; i++) {
                const startInput = document.getElementById(`start${i}`);
                const endInput = document.getElementById(`end${i}`);
                
                if (startInput && endInput && startInput.value && endInput.value) {
                    const start = parseFloat(startInput.value);
                    const end = parseFloat(endInput.value);
                    
                    if (start < end && end - start >= 2.0) {
                        segments.push([start, end]);
                    } else if (end - start < 2.0) {
                        showStatus(`Segment ${i} too short (${(end-start).toFixed(1)}s). Minimum 2 seconds required.`, 'error');
                        return;
                    } else {
                        showStatus(`Invalid segment ${i}: start time must be less than end time`, 'error');
                        return;
                    }
                }
            }

            if (segments.length === 0) {
                showStatus('No valid segments specified', 'error');
                return;
            }

            // Show summary
            let totalDuration = 0;
            let summary = `Trimming ${currentVideo.name}:\\n`;
            segments.forEach((seg, i) => {
                const duration = seg[1] - seg[0];
                totalDuration += duration;
                summary += `Segment ${i+1}: ${seg[0].toFixed(1)}s - ${seg[1].toFixed(1)}s (${duration.toFixed(1)}s)\\n`;
            });
            summary += `Total output duration: ${totalDuration.toFixed(1)}s`;

            if (!confirm(summary + '\\n\\nProceed with trimming?')) {
                return;
            }

            showStatus('Trimming video... This may take a few minutes.', 'info');

            // Send trim request
            fetch('/api/trim', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    video_name: currentVideo.name,
                    segments: segments
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showStatus(`Successfully trimmed ${currentVideo.name}!`, 'success');
                    setTimeout(() => {
                        loadVideos(currentBatch);
                    }, 2000);
                } else {
                    showStatus('Error trimming video: ' + data.error, 'error');
                }
            })
            .catch(error => {
                showStatus('Error trimming video: ' + error, 'error');
            });
        }

        function skipVideo(videoName) {
            if (confirm(`Skip trimming for ${videoName}?`)) {
                showStatus(`Skipped ${videoName}`, 'info');
                loadVideos(currentBatch);
            }
        }

        // Load batch info and first batch on page load
        loadBatchInfo();
    </script>
</body>
</html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def serve_video_list(self, batch_num=1):
        videos = self.trimmer.get_video_batch(batch_num)
        self.send_json_response(videos)
    
    def serve_batch_info(self):
        batch_info = self.trimmer.get_batch_info()
        self.send_json_response(batch_info)
    
    def serve_video_info(self, video_name):
        video_info = self.trimmer.get_video_details(video_name)
        if video_info:
            self.send_json_response(video_info)
        else:
            self.send_error(404)
    
    def serve_preview_frame(self, filename):
        preview_path = os.path.join(self.trimmer.preview_dir, filename)
        if os.path.exists(preview_path):
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg')
            self.end_headers()
            with open(preview_path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404)
    
    def handle_trim_request(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode())
            video_name = data['video_name']
            segments = data['segments']
            
            success = self.trimmer.trim_video(video_name, segments)
            
            if success:
                self.send_json_response({'success': True})
            else:
                self.send_json_response({'success': False, 'error': 'Trimming failed'})
                
        except Exception as e:
            self.send_json_response({'success': False, 'error': str(e)})
    
    def send_json_response(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

class WebVideoTrimmer:
    def __init__(self, input_dir="rau_so_seg_videos_redacted", output_base="Project"):
        self.input_dir = input_dir
        self.output_base = output_base
        self.output_dir = os.path.join(output_base, "trimmed_videos")
        self.preview_dir = os.path.join(output_base, "preview_frames")
        self.logs_dir = os.path.join(output_base, "logs")
        self.log_file = os.path.join(self.logs_dir, "trimming_log.csv")
        
        # Create directories
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.preview_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
        
        # Initialize log file
        self.init_log_file()
    
    def init_log_file(self):
        """Initialize CSV log file with headers if it doesn't exist."""
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'video_name', 'segment_number', 'start_time', 'end_time', 'duration'])
    
    def get_video_info(self, video_path):
        """Get video information using ffprobe."""
        try:
            # Get duration
            cmd_duration = [
                'ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
                '-of', 'csv=p=0', video_path
            ]
            duration_result = subprocess.run(cmd_duration, capture_output=True, text=True, check=True)
            duration = float(duration_result.stdout.strip())
            
            # Get video info
            cmd_info = [
                'ffprobe', '-v', 'quiet', '-show_entries', 
                'stream=width,height,r_frame_rate,codec_name',
                '-select_streams', 'v:0', '-of', 'csv=p=0', video_path
            ]
            info_result = subprocess.run(cmd_info, capture_output=True, text=True, check=True)
            info_parts = info_result.stdout.strip().split(',')
            
            width = info_parts[0] if len(info_parts) > 0 else 'unknown'
            height = info_parts[1] if len(info_parts) > 1 else 'unknown'
            fps = info_parts[2] if len(info_parts) > 2 else 'unknown'
            codec = info_parts[3] if len(info_parts) > 3 else 'unknown'
            
            return {
                'duration': duration,
                'width': width,
                'height': height,
                'fps': fps,
                'codec': codec,
                'size_mb': os.path.getsize(video_path) / (1024*1024)
            }
            
        except Exception as e:
            print(f"Error getting video info: {e}")
            return None
    
    def create_preview_frames(self, video_path, video_name, num_frames=6):
        """Create preview frames for a video."""
        try:
            video_info = self.get_video_info(video_path)
            if not video_info:
                return []
            
            duration = video_info['duration']
            preview_frames = []
            
            # Create frames at different intervals
            for i in range(num_frames):
                timestamp = (duration / (num_frames + 1)) * (i + 1)
                frame_filename = f"{video_name.replace('.mp4', '')}_frame_{i+1:02d}_{timestamp:.1f}s.jpg"
                frame_path = os.path.join(self.preview_dir, frame_filename)
                
                cmd = [
                    'ffmpeg', '-y', '-i', video_path,
                    '-ss', str(timestamp),
                    '-vframes', '1',
                    '-q:v', '2',
                    frame_path
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    preview_frames.append({
                        'filename': frame_filename,
                        'timestamp': timestamp
                    })
            
            return preview_frames
            
        except Exception as e:
            print(f"Error creating preview frames: {e}")
            return []
    
    def get_batch_info(self):
        """Get batch information."""
        video_files = sorted(glob.glob(os.path.join(self.input_dir, "*.mp4")))
        total_videos = len(video_files)
        batch_size = 5
        total_batches = (total_videos + batch_size - 1) // batch_size
        
        return {
            'total_videos': total_videos,
            'batch_size': batch_size,
            'total_batches': total_batches
        }
    
    def get_video_batch(self, batch_num=1, batch_size=5):
        """Get a specific batch of videos."""
        video_files = sorted(glob.glob(os.path.join(self.input_dir, "*.mp4")))
        
        start_idx = (batch_num - 1) * batch_size
        end_idx = start_idx + batch_size
        batch_files = video_files[start_idx:end_idx]
        
        videos = []
        for video_path in batch_files:
            video_name = os.path.basename(video_path)
            video_info = self.get_video_info(video_path)
            
            # Check if already processed
            output_path = os.path.join(self.output_dir, f"trimmed_{video_name}")
            processed = os.path.exists(output_path)
            
            if video_info:
                videos.append({
                    'name': video_name,
                    'duration': video_info['duration'],
                    'size_mb': video_info['size_mb'],
                    'width': video_info['width'],
                    'height': video_info['height'],
                    'processed': processed
                })
        
        batch_info = self.get_batch_info()
        
        return {
            'videos': videos,
            'batch_num': batch_num,
            'total_batches': batch_info['total_batches'],
            'total_videos': batch_info['total_videos']
        }
    
    def get_video_details(self, video_name):
        """Get detailed info for a specific video including preview frames."""
        video_path = os.path.join(self.input_dir, video_name)
        
        if not os.path.exists(video_path):
            return None
        
        video_info = self.get_video_info(video_path)
        if not video_info:
            return None
        
        # Create preview frames if they don't exist
        preview_frames = self.create_preview_frames(video_path, video_name)
        
        return {
            'name': video_name,
            'duration': video_info['duration'],
            'size_mb': video_info['size_mb'],
            'width': video_info['width'],
            'height': video_info['height'],
            'fps': video_info['fps'],
            'codec': video_info['codec'],
            'preview_frames': preview_frames
        }
    
    def trim_video(self, video_name, segments):
        """Trim a video based on specified segments."""
        try:
            video_path = os.path.join(self.input_dir, video_name)
            output_path = os.path.join(self.output_dir, f"trimmed_{video_name}")
            
            if not segments:
                print("No segments to trim")
                return False
            
            # Create temporary directory for segments
            with tempfile.TemporaryDirectory() as temp_dir:
                segment_files = []
                
                # Extract each segment
                for i, (start, end) in enumerate(segments):
                    segment_file = os.path.join(temp_dir, f"segment_{i:03d}.mp4")
                    
                    cmd = [
                        'ffmpeg', '-y', '-i', video_path,
                        '-ss', str(start),
                        '-t', str(end - start),
                        '-c', 'copy',  # Copy streams without re-encoding
                        segment_file
                    ]
                    
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    if result.returncode == 0:
                        segment_files.append(segment_file)
                        print(f"Extracted segment {i+1}: {start:.1f}s - {end:.1f}s")
                    else:
                        print(f"Failed to extract segment {i+1}")
                        return False
                
                if not segment_files:
                    return False
                
                # Concatenate segments
                if len(segment_files) == 1:
                    # Single segment, just copy
                    cmd = ['cp', segment_files[0], output_path]
                    result = subprocess.run(cmd, capture_output=True, text=True)
                else:
                    # Multiple segments, concatenate
                    concat_file = os.path.join(temp_dir, "concat_list.txt")
                    with open(concat_file, 'w') as f:
                        for segment_file in segment_files:
                            f.write(f"file '{segment_file}'\n")
                    
                    cmd = [
                        'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
                        '-i', concat_file,
                        '-c', 'copy',
                        output_path
                    ]
                    
                    result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    # Log segments
                    self.log_segments(video_name, segments)
                    print(f"Successfully trimmed {video_name}")
                    return True
                else:
                    print(f"Failed to concatenate segments for {video_name}")
                    return False
                    
        except Exception as e:
            print(f"Error trimming video {video_name}: {e}")
            return False
    
    def log_segments(self, video_name, segments):
        """Log trimmed segments to CSV file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(self.log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            for i, (start, end) in enumerate(segments):
                duration = end - start
                writer.writerow([timestamp, video_name, i+1, start, end, duration])

def main():
    if len(sys.argv) > 1:
        input_dir = sys.argv[1]
    else:
        input_dir = "rau_so_seg_videos_redacted"
    
    if not os.path.exists(input_dir):
        print(f"Error: Input directory '{input_dir}' not found")
        sys.exit(1)
    
    trimmer = WebVideoTrimmer(input_dir)
    
    # Create handler with trimmer instance
    def handler(*args, **kwargs):
        VideoTrimmerHandler(*args, trimmer=trimmer, **kwargs)
    
    server = HTTPServer(('localhost', 8080), handler)
    
    print("="*60)
    print("Medical Video Trimmer - Web Interface")
    print("="*60)
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {trimmer.output_dir}")
    print(f"Log file: {trimmer.log_file}")
    print()
    print("🌐 Web interface available at: http://localhost:8080")
    print()
    print("Instructions:")
    print("1. Open the URL above in your browser")
    print("2. Review preview frames for each video")
    print("3. Specify time ranges to KEEP (removing pre/post scope segments)")
    print("4. Trimmed videos will be saved with 'trimmed_' prefix")
    print()
    print("Press Ctrl+C to stop the server")
    print("="*60)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.shutdown()

if __name__ == "__main__":
    main()
