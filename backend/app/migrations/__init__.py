import os
import sys

# Get the current working directory
cwd = os.getcwd()

# Get the parent directory of the current working directory
parent_directory_path = os.path.dirname(cwd)

# Append the parent directory to the PATH
sys.path.append(parent_directory_path)
