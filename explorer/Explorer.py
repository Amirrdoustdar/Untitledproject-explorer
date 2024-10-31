import os

def explore(extension, folder_path):
    result = {}
    extension = extension.lower() 
    
    for root, _, files in os.walk(folder_path):
        count = 0
        for file in files:
            
            if file.lower().endswith(f".{extension}"):
                count += 1

        
        if count > 0:
            relative_path = os.path.relpath(root, start=os.getcwd())
            result[relative_path] = count

    return result
