import os
from pathlib import Path

def define_dir(root, *names):
    """Creates a directory and ensures it exists."""
    path = root
    for name in names:
        path = path / name 
    path.mkdir(parents=True, exist_ok=True)
    return path

# Get the root directory of the repository (parent of 'utils')
dir_proj = Path(__file__).resolve().parents[1]

# Define the paths for 'logs' and 'results' directories
dir_log_results = define_dir(dir_proj, "logs")  # Logs directory path
dir_results = define_dir(dir_proj, "results")  # Results directory path
dir_fulltexts = define_dir(dir_results, "fulltexts")  # Full-text articles directory path
dir_researcharticles = define_dir(dir_results, "researcharticles")  # Research articles directory path
dir_methods = define_dir(dir_results, "methods")  # Methods sections directory path
dir_data = define_dir(dir_proj, "data") # Data directory path
dir_processed = define_dir(dir_results, "cleanresults") # Processed data directory
dir_plots = define_dir(dir_proj, "plots")  # Directory for plots