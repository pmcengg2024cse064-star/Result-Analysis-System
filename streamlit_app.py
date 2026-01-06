"""
Streamlit Cloud/Docker Entry Point
This file serves as the main entry point for Streamlit deployments
"""

import sys
import os

# Add src directory to path for module imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # Import and run the main app
    from app import main
    main()
