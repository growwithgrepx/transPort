#!/usr/bin/env python3
"""
Script to clean up old test screenshots from the test_screenshots/ folder.
This helps prevent the folder from growing too large over time.
"""

import os
import glob
import time
import argparse
from datetime import datetime, timedelta
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def cleanup_screenshots(days_old=7, max_files=50, dry_run=False):
    """
    Clean up old test screenshots.
    
    Args:
        days_old (int): Remove files older than this many days
        max_files (int): Keep only this many most recent files
        dry_run (bool): If True, only show what would be deleted without actually deleting
    """
    screenshots_dir = "test_screenshots"
    
    if not os.path.exists(screenshots_dir):
        logger.info(f"Screenshots directory '{screenshots_dir}' does not exist. Nothing to clean.")
        return
    
    # Get all PNG and HTML files in the screenshots directory
    png_files = glob.glob(os.path.join(screenshots_dir, "*.png"))
    html_files = glob.glob(os.path.join(screenshots_dir, "*.html"))
    all_files = png_files + html_files
    
    if not all_files:
        logger.info("No screenshot files found to clean.")
        return
    
    logger.info(f"Found {len(all_files)} files in {screenshots_dir}")
    
    # Strategy 1: Remove files older than specified days
    cutoff_time = time.time() - (days_old * 24 * 60 * 60)
    old_files = []
    
    for file_path in all_files:
        file_time = os.path.getmtime(file_path)
        if file_time < cutoff_time:
            old_files.append((file_path, file_time))
    
    if old_files:
        logger.info(f"Found {len(old_files)} files older than {days_old} days:")
        for file_path, file_time in old_files:
            file_date = datetime.fromtimestamp(file_time).strftime('%Y-%m-%d %H:%M:%S')
            logger.info(f"  {os.path.basename(file_path)} (modified: {file_date})")
        
        if not dry_run:
            for file_path, _ in old_files:
                try:
                    os.remove(file_path)
                    logger.info(f"Deleted: {os.path.basename(file_path)}")
                except Exception as e:
                    logger.error(f"Failed to delete {file_path}: {e}")
        else:
            logger.info("DRY RUN: Files would be deleted (use --execute to actually delete)")
    else:
        logger.info(f"No files older than {days_old} days found.")
    
    # Strategy 2: Keep only the most recent files if we have too many
    remaining_files = [f for f in all_files if f not in [path for path, _ in old_files]]
    
    if len(remaining_files) > max_files:
        # Sort by modification time (newest first)
        remaining_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        files_to_remove = remaining_files[max_files:]
        
        logger.info(f"Keeping only {max_files} most recent files. Removing {len(files_to_remove)} older files:")
        for file_path in files_to_remove:
            file_time = os.path.getmtime(file_path)
            file_date = datetime.fromtimestamp(file_time).strftime('%Y-%m-%d %H:%M:%S')
            logger.info(f"  {os.path.basename(file_path)} (modified: {file_date})")
        
        if not dry_run:
            for file_path in files_to_remove:
                try:
                    os.remove(file_path)
                    logger.info(f"Deleted: {os.path.basename(file_path)}")
                except Exception as e:
                    logger.error(f"Failed to delete {file_path}: {e}")
        else:
            logger.info("DRY RUN: Files would be deleted (use --execute to actually delete)")
    
    # Show final count
    if not dry_run:
        final_count = len([f for f in glob.glob(os.path.join(screenshots_dir, "*")) if os.path.isfile(f)])
        logger.info(f"Cleanup complete. {final_count} files remaining in {screenshots_dir}")

def main():
    parser = argparse.ArgumentParser(description="Clean up old test screenshots")
    parser.add_argument("--days", type=int, default=3, 
                       help="Remove files older than this many days (default: 7)")
    parser.add_argument("--max-files", type=int, default=20,
                       help="Keep only this many most recent files (default: 50)")
    parser.add_argument("--dry-run", action="store_true",
                       help="Show what would be deleted without actually deleting")
    parser.add_argument("--execute", action="store_true",
                       help="Actually execute the cleanup (default is dry-run)")
    
    args = parser.parse_args()
    
    # Default to dry-run unless --execute is specified
    dry_run = not args.execute
    
    logger.info(f"Starting screenshot cleanup (dry-run: {dry_run})")
    logger.info(f"Settings: Remove files older than {args.days} days, keep max {args.max_files} files")
    
    cleanup_screenshots(days_old=args.days, max_files=args.max_files, dry_run=dry_run)

if __name__ == "__main__":
    main() 