import os
from tqdm import tqdm

def explore(extensions, folder_path):
    """
    Explore the folder structure to count files with specific extensions.

    :param extensions: A list of file extensions to look for (e.g., ['txt', 'py']).
    :param folder_path: The starting folder path for the exploration.
    :return: A dictionary where keys are relative paths and values are file counts.
    """
    result = {}
    extensions = [ext.lower() for ext in extensions]

    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"The folder path '{folder_path}' does not exist.")

    for root, _, files in tqdm(os.walk(folder_path), desc="Exploring folders"):
        count = 0
        for file in files:
            if any(file.lower().endswith(f".{ext}") for ext in extensions):
                count += 1

        if count > 0:
            relative_path = os.path.relpath(root, start=os.getcwd())
            result[relative_path] = count

    return result

def print_results(results):
    """
    Print the exploration results in a user-friendly format.

    :param results: Dictionary containing the directory paths and file counts.
    """
    print(f"{'Directory':<50} | {'Count':<5}")
    print("-" * 60)
    for path, count in results.items():
        print(f"{path:<50} | {count:<5}")

def main():
    """
    Main function to run the file exploration tool.
    """
    print("Welcome to the File Explorer Tool")
    folder_path = input("Enter the folder path to explore: ").strip()
    extensions = input("Enter the file extensions to search for (comma-separated): ").strip().split(",")
    extensions = [ext.strip() for ext in extensions if ext.strip()]

    if not extensions:
        print("Error: No extensions provided. Exiting.")
        return

    try:
        results = explore(extensions, folder_path)
        print_results(results)
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
