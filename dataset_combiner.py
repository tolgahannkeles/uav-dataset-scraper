import os
import shutil

# Define the source and destination directories
source_dir = 'dataset'
destination_dir = 'dataset-all'

# Create the destination directory if it doesn't exist
os.makedirs(destination_dir, exist_ok=True)

# Iterate over all subdirectories in the source directory
for subdir, _, files in os.walk(source_dir):
    for file in files:
        # Construct full file path
        file_path = os.path.join(subdir, file)
        # Move the file to the destination directory
        shutil.copy(file_path, os.path.join(destination_dir, file))

print(f"All images have been moved to {destination_dir}")