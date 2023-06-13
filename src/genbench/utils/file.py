from pathlib import Path


def get_repo_dir() -> Path:
    """Get the path to the repository."""
    return Path(__file__).parent.parent.parent.parent
