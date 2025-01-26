import os
import sys

# Get the absolute path to the project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the project root to Python path
sys.path.insert(0, project_root) 