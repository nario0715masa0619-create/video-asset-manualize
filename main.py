"""
Main entry point for VideoAsset Manualize MVP.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from video_asset_manualize.build_asset import app

if __name__ == "__main__":
    app()
