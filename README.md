# File Explorer Tool

A Python-based utility for exploring directories and counting files based on their extensions. This tool is interactive, user-friendly, and supports progress feedback during the directory traversal.

## Features

- **Search by File Extension:** Search for single or multiple file types.
- **Progress Feedback:** Displays a progress bar while exploring directories using `tqdm`.
- **Error Handling:** Ensures graceful handling of invalid inputs or inaccessible directories.
- **Formatted Results:** Presents file counts in a clean, tabular format.

## How It Works

1. **User Input:**
   - Enter the folder path to explore.
   - Provide one or more file extensions to search for, separated by commas (e.g., `txt, py, csv`).

2. **Directory Traversal:**
   - The script scans the specified folder and its subdirectories.
   - Counts files that match the given extensions.

3. **Output:**
   - Displays a table with relative directory paths and file counts.

## Usage

### Requirements

- Python 3.x
- `tqdm` library (Install using `pip install tqdm`)

### Running the Script

1. Save the script as `file_explorer.py`.
2. Open a terminal or command prompt.
3. Run the script with:
   ```bash
   python file_explorer.py
   ```
4. Follow the on-screen prompts:
   - Enter the folder path.
   - Specify the file extensions to search for.

### Example

#### Input:
```
Enter the folder path to explore: /path/to/directory
Enter the file extensions to search for (comma-separated): py, txt
```

#### Output:
```
Directory                                             | Count
------------------------------------------------------------
/path/to/directory                                    | 3    
/path/to/directory/subdir1                           | 5    
/path/to/directory/subdir2                           | 2    
```

## Code Overview

### Key Functions

1. **`explore(extensions, folder_path)`**
   - Traverses the folder structure.
   - Counts files matching the specified extensions.
   - Returns a dictionary of relative paths and file counts.

2. **`print_results(results)`**
   - Prints the results in a tabular format.

3. **`main()`**
   - Handles user input and calls the required functions.
   - Provides error handling for invalid inputs or inaccessible directories.

## Customization

- Modify the script to save results to a file (e.g., CSV or JSON).
- Add support for case-insensitive extension matching (already included).
- Extend functionality to filter by file size or modification date.

## License

This project is licensed under the MIT License. You are free to use, modify, and distribute this tool as per the license terms.

---

Feel free to contribute or suggest improvements!

