import os
import random

# Directory path containing the images
directory = None # '/Users/siddhant/Projects/finding-logos/data/train/images/train'

# Get all files in the directory
files = os.listdir(directory)

# Filter only .jpg files
jpg_files = [f for f in files if f.endswith('.jpg')]
print(jpg_files)

# Iterate over the .jpg files and rename them
for i, filename in enumerate(jpg_files):
    # Generate new filename
    new_filename = f'image_{i+1}.jpg'
    
    # Rename the file
    os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
    print(f'Renamed {filename} to {new_filename}')

print('All files renamed successfully.')
