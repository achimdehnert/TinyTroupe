"""
Configuration utilities for the enhanced group memory system.
"""
import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # App settings
    APP_NAME = "Enhanced Group Memory"
    VERSION = "1.0.0"
    
    # Paths
    ROOT_DIR = Path(__file__).parent.parent.parent
    DATA_DIR = ROOT_DIR / "data"
    
    # Memory settings
    MEMORY_MODEL = "all-MiniLM-L6-v2"
    MEMORY_CONSOLIDATION_THRESHOLD = 0.8
    
    # Analytics settings
    MAX_ANALYTICS_WINDOW = 100
    SENTIMENT_ANALYSIS_BATCH_SIZE = 10
    
    # UI settings
    THEME = {
        "primaryColor": "#FF4B4B",
        "backgroundColor": "#FFFFFF",
        "secondaryBackgroundColor": "#F0F2F6",
        "textColor": "#262730",
        "font": "sans serif"
    }
    
    @classmethod
    def get_env(cls, key: str, default: Any = None) -> Any:
        """Get environment variable with fallback to default."""
        return os.getenv(key, default)
    
    @classmethod
    def setup_directories(cls) -> None:
        """Create necessary directories if they don't exist."""
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
        
    @classmethod
    def get_theme(cls) -> Dict[str, str]:
        """Get the UI theme configuration."""
        return cls.THEME
