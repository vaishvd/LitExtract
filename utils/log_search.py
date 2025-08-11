from utils.config import dir_log_results
from datetime import datetime

def keywords_to_ids(keywords, pmc_ids, log_file_path):
    """
    Log the search keywords and PMC IDs to a log file.
    
    Args:
        keywords (List[str]): Keywords used for the search.
        pmc_ids (List[str]): List of retrieved PMC IDs.
        log_file_path (Path): Path to the log file.
    """
    with open(log_file_path, 'a') as log_file:
        log_file.write(f"Search Query: {' AND '.join(keywords)}\n")
        log_file.write(f"Found {len(pmc_ids)} articles\n")
        log_file.write(f"PMC IDs Found: {', '.join([f'PMC{pmc_id}' for pmc_id in pmc_ids])}\n")
        log_file.write(f"Search Time: {datetime.now()}\n\n")

