import os
import pandas as pd
from typing import List, Dict, Any
import pathlib

# Directory for temporary data files
TEMP_DIR = pathlib.Path("./temp_data")
TEMP_DIR.mkdir(exist_ok=True)

def save_data_to_csv(data: List[Dict[str, Any]], dataset_id: str) -> pathlib.Path:
    """
    Save generated data to a CSV file.

    Args:
        data: List of dictionaries containing the generated data
        dataset_id: Unique identifier for the dataset

    Returns:
        Path to the saved CSV file
    """
    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Create the file path
    file_path = TEMP_DIR / f"{dataset_id}.csv"

    # Save to CSV
    df.to_csv(file_path, index=False)

    return file_path

def delete_csv_file(dataset_id: str) -> bool:
    """
    Delete a CSV file for a given dataset ID.

    Args:
        dataset_id: Unique identifier for the dataset

    Returns:
        True if the file was deleted, False otherwise
    """
    file_path = TEMP_DIR / f"{dataset_id}.csv"

    if file_path.exists():
        file_path.unlink()
        return True

    return False

def cleanup_old_files(max_age_hours: int = 24) -> int:
    """
    Clean up CSV files older than the specified age.

    Args:
        max_age_hours: Maximum age of files in hours

    Returns:
        Number of files deleted
    """
    import time
    from datetime import datetime, timedelta

    now = time.time()
    count = 0

    for file_path in TEMP_DIR.glob("*.csv"):
        # Get file modification time
        mtime = file_path.stat().st_mtime

        # Delete if older than max age
        if now - mtime > max_age_hours * 3600:
            file_path.unlink()
            count += 1

    return count