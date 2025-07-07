#!/usr/bin/env python3

"""
run_tests.py
---------------------------------
Convenience launcher for running all Pytest test suites.
"""

import sys
import subprocess

def main():
    # Allow passing optional arguments to pytest
    args = sys.argv[1:]  
    cmd = ["pytest"] + args

    # Call pytest as a subprocess
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    main()