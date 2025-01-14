import os
import fnmatch
import csv
import json
import zipfile
import pandas as pd
import logging
from datetime import datetime
from tqdm import tqdm
import stat
import unittest

# Logging configuration
logging.basicConfig(filename='explorer.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Dictionary to store activities
activity_log = []

def log_activity(action, details):
    """Save activities to a dictionary and JSON file"""
    activity = {
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "action": action,
        "details": details
    }
    activity_log.append(activity)
    with open("activity_log.json", "w", encoding="utf-8") as f:
        json.dump(activity_log, f, indent=4)

def explore(extension, folder_path, name_pattern=None, multiple_extensions=None, interactive=False, 
            start_date=None, end_date=None, search_term=None, min_size=None, max_size=None, 
            depth=None, writable=False, executable=False):
    result = {}
    
    if multiple_extensions:
        extensions = [ext.lower() for ext in multiple_extensions]
    else:
        extensions = [extension.lower()]

    if interactive:
        folder_path = input("Enter the folder path: ")
        extensions = input("Enter the file extensions (comma-separated): ").lower().split(',')
        name_pattern = input("Enter a name pattern (or leave blank for none): ") or None
        search_term = input("Enter a search term (or leave blank for none): ") or None
        min_size = int(input("Enter minimum file size in bytes (or leave blank for none): ") or 0)
        max_size = int(input("Enter maximum file size in bytes (or leave blank for none): ") or float('inf'))
        depth = int(input("Enter search depth (or leave blank for none): ") or None)
        writable = input("Search for writable files only? (y/n): ").lower() == 'y'
        executable = input("Search for executable files only? (y/n): ").lower() == 'y'

    log_activity("Explore Started", {
        "folder_path": folder_path,
        "extensions": extensions,
        "name_pattern": name_pattern,
        "search_term": search_term,
        "min_size": min_size,
        "max_size": max_size,
        "depth": depth,
        "writable": writable,
        "executable": executable
    })

    try:
        for root, _, files in tqdm(os.walk(folder_path), desc="Searching", unit="folder"):
            current_depth = root[len(folder_path):].count(os.sep)
            if depth is not None and current_depth > depth:
                continue

            count = 0
            total_size = 0
            matched_files = []

            for file in files:
                try:
                    file_path = os.path.join(root, file)
                    file_ext = os.path.splitext(file)[-1].lower()
                    last_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
                    size = os.path.getsize(file_path)
                    mode = os.stat(file_path).st_mode

                    # Apply filters
                    if (file_ext in extensions and
                        (not name_pattern or fnmatch.fnmatch(file, name_pattern)) and
                        (not start_date or last_modified >= start_date) and
                        (not end_date or last_modified <= end_date) and
                        (not search_term or search_in_file(file_path, search_term)) and
                        (not min_size or size >= min_size) and
                        (not max_size or size <= max_size) and
                        (not writable or os.access(file_path, os.W_OK)) and
                        (not executable or os.access(file_path, os.X_OK))):

                        count += 1
                        total_size += size
                        matched_files.append({"name": file, "size": size, "last_modified": last_modified.strftime('%Y-%m-%d %H:%M:%S')})
                except (FileNotFoundError, PermissionError, UnicodeDecodeError) as e:
                    logging.warning(f"Error accessing file {file}: {e}")
                    log_activity("File Access Error", {
                        "file": file,
                        "error": str(e)
                    })

            if count > 0:
                relative_path = os.path.relpath(root, start=os.getcwd())
                result[relative_path] = {"count": count, "total_size": total_size, "files": matched_files}
    except (FileNotFoundError, PermissionError) as e:
        logging.error(f"Error accessing folder {folder_path}: {e}")
        log_activity("Folder Access Error", {
            "folder_path": folder_path,
            "error": str(e)
        })

    log_activity("Explore Completed", {
        "total_folders": len(result),
        "total_files": sum(details["count"] for details in result.values())
    })

    return result

def search_in_file(file_path, search_term):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return search_term in content
    except UnicodeDecodeError:
        return False  # For binary or non-text files

def generate_report(data, report_file="report.csv", format="csv"):
    try:
        if format == "csv":
            with open(report_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Folder Path", "File Count", "Total Size (bytes)", "File Name", "File Size (bytes)", "Last Modified"])

                for folder, details in data.items():
                    for file in details["files"]:
                        writer.writerow([
                            folder,
                            details["count"],
                            details["total_size"],
                            file["name"],
                            file["size"],
                            file["last_modified"]
                        ])
        elif format == "json":
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        elif format == "excel":
            rows = []
            for folder, details in data.items():
                for file in details["files"]:
                    rows.append([folder, details["count"], details["total_size"], file["name"], file["size"], file["last_modified"]])
            
            df = pd.DataFrame(rows, columns=["Folder Path", "File Count", "Total Size (bytes)", "File Name", "File Size (bytes)", "Last Modified"])
            df.to_excel(report_file, index=False)
        
        log_activity("Report Generated", {
            "report_file": report_file,
            "format": format
        })
    except IOError as e:
        logging.error(f"Error writing to report file: {e}")
        log_activity("Report Generation Error", {
            "report_file": report_file,
            "error": str(e)
        })

def compress_report(report_file, zip_file):
    try:
        with zipfile.ZipFile(zip_file, 'w') as zipf:
            zipf.write(report_file, os.path.basename(report_file))
        log_activity("Report Compressed", {
            "report_file": report_file,
            "zip_file": zip_file
        })
    except IOError as e:
        logging.error(f"Error compressing report file: {e}")
        log_activity("Report Compression Error", {
            "report_file": report_file,
            "error": str(e)
        })

def main():
    # Example usage of the explore function
    folder_path = "."  # Current directory
    extensions = [".py", ".txt"]  # Example of multiple extensions
    data = explore(
        extension=None,
        folder_path=folder_path,
        multiple_extensions=extensions,
        name_pattern="*example*",
        interactive=False,
        start_date=datetime(2023, 1, 1),
        end_date=datetime(2023, 12, 31),
        search_term="example",
        min_size=1024,  # Minimum 1KB
        max_size=1048576,  # Maximum 1MB
        depth=2,  # Search depth of 2 subfolders
        writable=False,
        executable=False
    )

    # Sort results by total file size
    sorted_data = dict(sorted(data.items(), key=lambda item: item[1]["total_size"], reverse=True))

    # Generate reports in different formats
    generate_report(sorted_data, report_file="report.csv", format="csv")
    generate_report(sorted_data, report_file="report.json", format="json")
    generate_report(sorted_data, report_file="report.xlsx", format="excel")

    # Compress the report
    compress_report("report.csv", "report.zip")

# Unit tests
class TestExplorer(unittest.TestCase):
    def test_explore(self):
        data = explore(extension=".py", folder_path=".", name_pattern="*example*")
        self.assertGreater(len(data), 0)

if __name__ == "__main__":
    main()
    unittest.main()