#!/usr/bin/env python
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Now run the seed script
from app.scripts.seed_questions import seed

if __name__ == "__main__":
    seed()
