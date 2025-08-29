import sys
from pathlib import Path

# Ensure src directory is on the path for tests without installation
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
