from datetime import datetime
import os

def generate_filename(creativename: str, directory: str, ext: str) -> str:
    
    """
    Create a full file path by combining a directory, a creative name,
    and a timestamp-based filename.

    Args:
        creativename (str): Custom name to include in the file.
        directory (str): Directory path where the file should be saved.

    Returns:
        str: Full path like 'path/to/dir/salesreport_20250721_213045.csv'
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{creativename}_{timestamp}.{ext}"
    full_path = os.path.join(directory, filename)
    return full_path
