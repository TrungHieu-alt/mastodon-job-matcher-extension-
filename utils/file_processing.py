"""File processing utilities."""

import os
import uuid
from pathlib import Path
from typing import List, Optional
from loguru import logger


def get_supported_file_extensions() -> List[str]:
    """Get list of supported file extensions."""
    return ['.pdf', '.png', '.jpg', '.jpeg']


def find_cv_files(folder_path: str) -> List[Path]:
    """Find all CV files in a folder."""
    folder = Path(folder_path)
    if not folder.exists():
        logger.warning(f"Folder does not exist: {folder_path}")
        return []
    
    cv_files = []
    for ext in get_supported_file_extensions():
        cv_files.extend(folder.glob(f"*{ext}"))
        cv_files.extend(folder.glob(f"*{ext.upper()}"))
    
    return sorted(cv_files)


def generate_unique_id(prefix: str = "id") -> str:
    """Generate a unique ID with prefix."""
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def get_file_size(file_path: Path) -> int:
    """Get file size in bytes."""
    try:
        return file_path.stat().st_size
    except Exception as e:
        logger.error(f"Error getting file size for {file_path}: {e}")
        return 0


def validate_file_type(file_path: Path) -> bool:
    """Validate if file type is supported."""
    return file_path.suffix.lower() in get_supported_file_extensions()


def create_temp_file_path(owner: str, file_extension: str) -> str:
    """Create temporary file path for processing."""
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)
    
    filename = f"{owner}_{uuid.uuid4().hex[:6]}{file_extension}"
    return str(temp_dir / filename)


def cleanup_temp_file(file_path: str) -> bool:
    """Clean up temporary file."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Cleaned up temp file: {file_path}")
            return True
        return True
    except Exception as e:
        logger.error(f"Error cleaning up temp file {file_path}: {e}")
        return False
