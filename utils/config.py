import os
from pathlib import Path

def define_dir(root, *names):
    """Creates a directory and ensures it exists."""
    path = root
    for name in names:
        path = path / name  # use pathlib's '/' operator to join paths
    path.mkdir(parents=True, exist_ok=True)
    return path

# Get the current directory where the script is executed
dir_proj = Path.cwd().parent

# Define the paths for 'logs' and 'results' directories
dir_log_results = define_dir(dir_proj, "logs")  # Logs directory path
dir_results = define_dir(dir_proj, "results")  # Results directory path
dir_fulltexts = define_dir(dir_results, "fulltexts")  # Full-text articles directory path
dir_researcharticles = define_dir(dir_results, "researcharticles")  # Research articles directory path
dir_methods = define_dir(dir_results, "methods")  # Methods sections directory path
dir_validation = define_dir(dir_proj, "validation")  # Validation directory
dir_valpapers = define_dir(dir_validation, "valpapers") # Input papers for validation directory
dir_valmethods = define_dir(dir_validation, "valmethods") # Methods for validation papers


dir_stepsjson = define_dir(dir_results, "preprocessingsteps_extracted") #JSON files containing preprocessing steps for each article