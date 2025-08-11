from utils.article_fetcher import search_pmc_by_keyword, fetch_full_text_pmc
from utils.saveas import save_xml
from utils.log_search import keywords_to_ids
from utils.config import dir_fulltexts, dir_log_results


keywords = ['Mobile-EEG', 'Gait']
log_file_path = dir_log_results.joinpath("keyword_overview.txt")

# Step 1: Search for PMC IDs using AND logic
pmc_ids = search_pmc_by_keyword(keywords)

if pmc_ids:
    print(f"Found PMC IDs: {pmc_ids}")
    
    # Step 2: Fetch full text for each PMC ID and save it as XML
    for pmc_id in pmc_ids:
        full_text = fetch_full_text_pmc(pmc_id)
        if full_text:
            save_xml(pmc_id, full_text, dir_fulltexts)
        else:
            print(f"Could not fetch full text for PMC ID: {pmc_id}")
    
    # Step 3: Log the search results
    keywords_to_ids(keywords, pmc_ids, log_file_path)
    print("Search results logged successfully.")
else:
    print("No PMC IDs found for the given keywords.")

