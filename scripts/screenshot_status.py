#!/usr/bin/env python3
"""
Script to show the current status of the test_screenshots folder.
"""

import os
import glob
import time
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_screenshot_status():
    """Get the current status of the test_screenshots folder"""
    screenshots_dir = "test_screenshots"
    
    if not os.path.exists(screenshots_dir):
        logger.info(f"Screenshots directory '{screenshots_dir}' does not exist.")
        return
    
    # Get all files
    png_files = glob.glob(os.path.join(screenshots_dir, "*.png"))
    html_files = glob.glob(os.path.join(screenshots_dir, "*.html"))
    all_files = png_files + html_files
    
    if not all_files:
        logger.info("No screenshot files found.")
        return
    
    # Calculate total size
    total_size = sum(os.path.getsize(f) for f in all_files)
    total_size_mb = total_size / (1024 * 1024)
    
    # Get file ages
    now = time.time()
    file_ages = []
    for file_path in all_files:
        file_time = os.path.getmtime(file_path)
        age_hours = (now - file_time) / 3600
        file_ages.append((file_path, age_hours))
    
    # Sort by age (oldest first)
    file_ages.sort(key=lambda x: x[1])
    
    logger.info(f"Screenshot folder status:")
    logger.info(f"  Total files: {len(all_files)}")
    logger.info(f"  PNG files: {len(png_files)}")
    logger.info(f"  HTML files: {len(html_files)}")
    logger.info(f"  Total size: {total_size_mb:.2f} MB")
    logger.info(f"  Average file size: {total_size_mb/len(all_files):.2f} MB")
    
    if file_ages:
        oldest_file = file_ages[0]
        newest_file = file_ages[-1]
        
        logger.info(f"  Oldest file: {os.path.basename(oldest_file[0])} ({oldest_file[1]:.1f} hours old)")
        logger.info(f"  Newest file: {os.path.basename(newest_file[0])} ({newest_file[1]:.1f} hours old)")
    
    # Show recent files (last 5)
    logger.info(f"\nRecent files:")
    for file_path, age_hours in file_ages[-5:]:
        file_size = os.path.getsize(file_path) / 1024  # KB
        logger.info(f"  {os.path.basename(file_path)} ({age_hours:.1f}h old, {file_size:.1f} KB)")

def main():
    get_screenshot_status()

if __name__ == "__main__":
    main() 