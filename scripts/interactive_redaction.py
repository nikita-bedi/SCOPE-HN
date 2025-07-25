#!/usr/bin/env python3
"""
Interactive PHI redaction tool using matplotlib for frame display and bounding box selection.
"""

import os
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Button
import numpy as np
from PIL import Image
import glob

class RedactionSelector:
    def __init__(self):
        self.coordinates = {}
        self.current_video = None
        self.current_frame_path = None
        self.video_files = []
        self.current_index = 0
        self.bbox = None
        self.rect = None
        self.start_point = None
        
        # Load existing coordinates if available
        if os.path.exists('redaction_coordinates.json'):
            with open('redaction_coordinates.json', 'r') as f:
                self.coordinates = json.load(f)
        
        # Get list of sample frames
        self.frame_files = sorted(glob.glob('sample_frames/*.jpg'))
        self.video_files = [os.path.basename(f).replace('_sample.jpg', '.mp4') for f in self.frame_files]
        
        if not self.frame_files:
            print("No sample frames found! Please run extract_frames.py first.")
            return
        
        print(f"Found {len(self.frame_files)} videos to process")
        self.setup_plot()
        self.load_current_frame()
    
    def setup_plot(self):
        """Set up the matplotlib interface."""
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.fig.suptitle('PHI Redaction - Click and drag to select redaction area', fontsize=14)
        
        # Create buttons
        ax_next = plt.axes([0.81, 0.05, 0.08, 0.04])
        ax_prev = plt.axes([0.71, 0.05, 0.08, 0.04])
        ax_save = plt.axes([0.61, 0.05, 0.08, 0.04])
        ax_clear = plt.axes([0.51, 0.05, 0.08, 0.04])
        ax_export = plt.axes([0.41, 0.05, 0.08, 0.04])
        
        self.btn_next = Button(ax_next, 'Next')
        self.btn_prev = Button(ax_prev, 'Previous')
        self.btn_save = Button(ax_save, 'Save')
        self.btn_clear = Button(ax_clear, 'Clear')
        self.btn_export = Button(ax_export, 'Export JSON')
        
        # Connect button events
        self.btn_next.on_clicked(self.next_video)
        self.btn_prev.on_clicked(self.prev_video)
        self.btn_save.on_clicked(self.save_coordinates)
        self.btn_clear.on_clicked(self.clear_bbox)
        self.btn_export.on_clicked(self.export_json)
        
        # Connect mouse events
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
    
    def load_current_frame(self):
        """Load and display the current frame."""
        if self.current_index >= len(self.frame_files):
            print("All videos processed!")
            return
        
        self.current_frame_path = self.frame_files[self.current_index]
        self.current_video = self.video_files[self.current_index]
        
        # Load image
        img = Image.open(self.current_frame_path)
        img_array = np.array(img)
        
        # Clear previous plot
        self.ax.clear()
        self.ax.imshow(img_array)
        self.ax.set_title(f'Video: {self.current_video} ({self.current_index + 1}/{len(self.video_files)})')
        
        # Load existing bounding box if available
        if self.current_video in self.coordinates:
            coords = self.coordinates[self.current_video]
            self.draw_bbox(coords['x'], coords['y'], coords['width'], coords['height'])
        
        # Update progress info
        completed = len(self.coordinates)
        progress_text = f"Progress: {completed}/{len(self.video_files)} videos processed"
        self.ax.text(0.02, 0.98, progress_text, transform=self.ax.transAxes, 
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7),
                    verticalalignment='top')
        
        if self.current_video in self.coordinates:
            coords = self.coordinates[self.current_video]
            coord_text = f"Saved: x={coords['x']}, y={coords['y']}, w={coords['width']}, h={coords['height']}"
            self.ax.text(0.02, 0.02, coord_text, transform=self.ax.transAxes,
                        bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen", alpha=0.7),
                        verticalalignment='bottom')
        
        plt.draw()
    
    def draw_bbox(self, x, y, width, height):
        """Draw bounding box on the image."""
        if self.rect:
            self.rect.remove()
        
        self.rect = patches.Rectangle((x, y), width, height, 
                                    linewidth=2, edgecolor='red', 
                                    facecolor='red', alpha=0.3)
        self.ax.add_patch(self.rect)
        self.bbox = {'x': x, 'y': y, 'width': width, 'height': height}
    
    def on_press(self, event):
        """Handle mouse press event."""
        if event.inaxes != self.ax:
            return
        self.start_point = (event.xdata, event.ydata)
    
    def on_release(self, event):
        """Handle mouse release event."""
        if event.inaxes != self.ax or not self.start_point:
            return
        
        end_point = (event.xdata, event.ydata)
        
        # Calculate bounding box
        x = min(self.start_point[0], end_point[0])
        y = min(self.start_point[1], end_point[1])
        width = abs(end_point[0] - self.start_point[0])
        height = abs(end_point[1] - self.start_point[1])
        
        if width > 5 and height > 5:  # Minimum size
            self.draw_bbox(int(x), int(y), int(width), int(height))
            plt.draw()
        
        self.start_point = None
    
    def on_motion(self, event):
        """Handle mouse motion for live preview."""
        if not self.start_point or event.inaxes != self.ax:
            return
        
        # Draw temporary rectangle
        if hasattr(self, 'temp_rect') and self.temp_rect:
            self.temp_rect.remove()
        
        x = min(self.start_point[0], event.xdata)
        y = min(self.start_point[1], event.ydata)
        width = abs(event.xdata - self.start_point[0])
        height = abs(event.ydata - self.start_point[1])
        
        self.temp_rect = patches.Rectangle((x, y), width, height,
                                         linewidth=1, edgecolor='blue',
                                         facecolor='none', linestyle='--')
        self.ax.add_patch(self.temp_rect)
        plt.draw()
    
    def next_video(self, event):
        """Go to next video."""
        if self.current_index < len(self.video_files) - 1:
            self.current_index += 1
            self.load_current_frame()
    
    def prev_video(self, event):
        """Go to previous video."""
        if self.current_index > 0:
            self.current_index -= 1
            self.load_current_frame()
    
    def save_coordinates(self, event):
        """Save current bounding box coordinates."""
        if not self.bbox:
            print("No bounding box selected!")
            return
        
        self.coordinates[self.current_video] = {
            'x': self.bbox['x'],
            'y': self.bbox['y'],
            'width': self.bbox['width'],
            'height': self.bbox['height'],
            'video_file': self.current_video
        }
        
        # Save to file immediately
        with open('redaction_coordinates.json', 'w') as f:
            json.dump(self.coordinates, f, indent=2)
        
        print(f"Saved coordinates for {self.current_video}")
        self.load_current_frame()  # Refresh display
    
    def clear_bbox(self, event):
        """Clear current bounding box."""
        if self.rect:
            self.rect.remove()
            self.rect = None
        self.bbox = None
        plt.draw()
    
    def export_json(self, event):
        """Export all coordinates to JSON file."""
        with open('redaction_coordinates.json', 'w') as f:
            json.dump(self.coordinates, f, indent=2)
        print(f"Exported coordinates for {len(self.coordinates)} videos to redaction_coordinates.json")
    
    def run(self):
        """Start the interactive session."""
        print("\nInstructions:")
        print("1. Click and drag on the image to select redaction area")
        print("2. Click 'Save' to save coordinates for current video")
        print("3. Use 'Next'/'Previous' to navigate between videos")
        print("4. Click 'Export JSON' when done to save all coordinates")
        print("5. Close the window when finished")
        plt.show()

def main():
    if not os.path.exists('sample_frames'):
        print("Sample frames directory not found!")
        print("Please run: python3 extract_frames.py")
        return
    
    selector = RedactionSelector()
    selector.run()

if __name__ == "__main__":
    main()
