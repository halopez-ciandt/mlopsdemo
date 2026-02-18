"""Pytest configuration for mlopsdemo tests."""
import sys
from pathlib import Path

# Add project root and src directory to Python path for module imports
project_root = Path(__file__).parent.parent
src_path = project_root / "src"

# Add project root first (so "src" can be found as a package)
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Add src directory (for direct imports like "from src.models...")
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))
