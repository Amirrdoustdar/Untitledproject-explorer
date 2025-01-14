# File Explorer Tool

A Python-based utility for exploring directories, filtering files, and generating reports. This tool combines user-friendliness with advanced features, making it suitable for beginners and power users alike.

---

## Features

### Core Features
- **Search by File Extension**: Look for single or multiple file types.
- **Interactive Mode**: Allows users to input folder paths and file extensions dynamically.
- **Progress Feedback**: Displays a progress bar using `tqdm` during directory traversal.
- **Error Handling**: Handles invalid inputs and inaccessible directories gracefully.
- **Formatted Results**: Presents file counts in a clean, tabular format.

### Advanced Features
- **Detailed Logging**: Logs activities and errors for auditing and debugging.
- **Flexible Filters**:
  - File size range (e.g., min/max size).
  - Modification date range.
  - Writable or executable file filters.
  - Keyword search within file contents.
- **Comprehensive Reporting**:
  - Export results to CSV, JSON, or Excel.
  - Compress reports into ZIP files for easy sharing.

---

## How It Works

### User Input
1. Enter the folder path to explore.
2. Provide one or more file extensions to search for (e.g., `py, txt, csv`).
3. Optionally specify filters like name patterns, size limits, or date ranges.

### Directory Traversal
- The script scans the specified folder and its subdirectories.
- Counts files that match the provided filters and extensions.

### Output
- Displays results in a table with relative directory paths, file counts, and sizes.
- Generates detailed reports for further analysis.

---

## Usage

### Requirements
- Python 3.x
- Libraries: Install dependencies using:
  ```bash
  pip install pandas tqdm openpyxl
  ```

### Running the Script
1. Save the script as `Explorer.py`.
2. Open a terminal or command prompt.
3. Run the script with:
   ```bash
   python Explorer.py
   ```
4. Follow the on-screen prompts for interactive mode, or customize the `main` function for predefined inputs.

### Example

#### Input:
```plaintext
Enter the folder path to explore: /path/to/directory
Enter the file extensions to search for (comma-separated): py, txt
```

#### Output:
```plaintext
Directory                                             | Count
------------------------------------------------------------
/path/to/directory                                    | 3    
/path/to/directory/subdir1                           | 5    
/path/to/directory/subdir2                           | 2    
```

---

## Advanced Example with Filters

```python
from datetime import datetime

results = explore(
    extension=None,
    folder_path="/path/to/folder",
    multiple_extensions=[".py", ".txt"],
    name_pattern="*example*",
    start_date=datetime(2023, 1, 1),
    end_date=datetime(2023, 12, 31),
    min_size=1024,  # Minimum 1KB
    max_size=1048576,  # Maximum 1MB
    depth=2,
    writable=False,
    executable=False
)

# Generate reports
generate_report(results, report_file="report.csv", format="csv")
compress_report("report.csv", "report.zip")
```

---

## Code Overview

### Key Functions

- `explore(extension, folder_path, ...)`: Traverses directories and filters files based on criteria.
- `generate_report(data, report_file, format)`: Creates reports in CSV, JSON, or Excel formats.
- `compress_report(report_file, zip_file)`: Compresses report files into ZIP format.
- `log_activity(action, details)`: Logs actions and errors to a JSON file.

### Main Function
- Handles user inputs and calls the necessary functions.
- Provides error handling and feedback during execution.

---

## Customization
- Save results to additional formats like YAML or plain text.
- Extend filters to include file owners or permissions.
- Enhance reporting to include visual charts or graphs.

---

## Testing
- Unit tests are included to validate core functionality:
  ```bash
  python -m unittest Explorer.py
  ```

---

## License
This project is licensed under the MIT License. Feel free to use, modify, and distribute this tool as per the license terms.

---

Contributions and feedback are welcome! Submit issues or pull requests to help improve this tool.

