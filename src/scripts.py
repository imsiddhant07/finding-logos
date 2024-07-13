import os

def get_parent_directory_before_keyword(file_path, keyword):
    """
    Get the parent directory path before a specific keyword in a file path.

    Args:
        file_path (str): Full file path containing the keyword.
        keyword (str): Keyword to find the directory path before.

    Returns:
        str: Parent directory path before the keyword.
    """
    # Find the position of the last occurrence of the keyword
    index = file_path.rfind(keyword)
    
    # If keyword not found, return the original file_path
    if index == -1:
        return file_path
    
    # Get the substring before the keyword
    parent_directory = file_path[:index]
    
    # Clean up path using os.path.dirname to remove any extra slashes
    parent_directory = os.path.dirname(parent_directory)
    
    return parent_directory

# Example usage:
# Example usage:
target_path = '/Users/siddhant/Projects/finding-logos/data/inference/3975/extracted_frames/frame_000002.jpg'
target_dir_name = 'extracted_frames'
parent_directory = get_parent_directory_before_keyword(target_path, target_dir_name)
print(parent_directory)
