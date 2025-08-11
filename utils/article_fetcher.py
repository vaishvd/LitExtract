import os
import requests
import xml.etree.ElementTree as ET
import re

# --- MeSH and Query Optimization Functions ---
def get_mesh_terms(keyword):
    """Retrieve relevant MeSH terms for a keyword.
    This function takes a keyword and retrieves relevant Medical Subject Headings (MeSH) terms
    from the NCBI Entrez database. It first searches for the keyword in the MeSH database and 
    retrieves up to three unique identifiers (UIDs). It then fetches the detailed MeSH terms 
    associated with these UIDs and returns a list of up to five unique MeSH terms.
    Args:
        keyword (str): The keyword to search for in the MeSH database.
    Returns:
        list: A list of up to five relevant MeSH terms. If no terms are found or an error occurs, 
        an empty list is returned.
    Raises:
        Exception: If there is an error during the HTTP request or XML parsing, an exception is caught 
        and an error message is printed.
    """
    """Retrieve relevant MeSH terms for a keyword"""
    try:
        search_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=mesh&term={keyword}&retmode=xml"
        search_response = requests.get(search_url, timeout=10)
        search_root = ET.fromstring(search_response.content)
        
        query_translation = search_root.find('.//QueryTranslation')
        if query_translation is None:
            return []

        translated_query = query_translation.text
        terms = re.findall(r'"([^"]+)"\[MeSH Terms\]', translated_query)
        
        return terms[:5]
    
    except Exception as e:
        print(f"MeSH retrieval error: {e}")
        return []

def build_enhanced_query(keywords):
    """Build optimized query using MeSH terms and LLM"""
    # Build base query with MeSH terms
    query_parts = []
    for keyword in keywords:
        terms = [f'"{keyword}"[Title/Abstract]'] + [f'"{term}"[MeSH Terms]' for term in get_mesh_terms(keyword)]
        query_parts.append(f'({" OR ".join(terms)})')
    
    base_query = " AND ".join(query_parts)
    
    return base_query

# --- Modified Search Function ---
def search_pmc_by_keyword(keywords):
    """
    Search PMC with MeSH-optimized queries using LLM-enhanced terms.
    Args:
        keywords (str): The keywords to search for in PMC.
    Returns:
        list: A list of PMC IDs that match the search query.
    Raises:
        requests.exceptions.RequestException: If there is an error with the HTTP request.
        xml.etree.ElementTree.ParseError: If there is an error parsing the XML response.
        Exception: For any other unexpected errors.
    """
    """Search PMC with MeSH-optimized queries using LLM-enhanced terms"""
    try:
        # Build enhanced query
        query = build_enhanced_query(keywords)
        encoded_query = requests.utils.quote(query)
        url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&term={encoded_query}&retmode=xml&retmax=10000"

        response = requests.get(url)
        response.raise_for_status()

        # Parse XML properly
        root = ET.fromstring(response.content)
        pmc_ids = [id_tag.text for id_tag in root.findall('.//IdList/Id')]
        
        print(f"Total articles found: {len(pmc_ids)}")
        return pmc_ids

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except ET.ParseError as e:
        print(f"XML parsing error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return []

# --- Existing Full-Text Function (unchanged) ---
def fetch_full_text_pmc(pmc_id):
    """
    Fetches the full text of an article from PubMed Central (PMC) using the provided PMC ID.

    Args:
        pmc_id (str): The PubMed Central ID of the article to fetch.

    Returns:
        str: The full text of the article in XML format if the request is successful.
        None: If the request fails (i.e., the status code is not 200).
    """
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id={pmc_id}&retmode=xml"
    response = requests.get(url)
    return response.text if response.status_code == 200 else None

def is_research_article(file_path):
    """
    Check if an XML file is a research article based on its content.
    
    Args:
        file_path (Path): Path to the XML file.
    
    Returns:
        bool: True if the file is a research article, False otherwise.
    """
    try:
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Find the article element and check its type
        article_element = root.find('.//article')
        if article_element is not None:
            article_type = article_element.attrib.get('article-type')
            if article_type == 'research-article':
                return True

    except ET.ParseError as e:
        # Handle XML parsing errors
        print(f"Error parsing file {file_path}: {e}")
    except Exception as e:
        # Handle any other unexpected errors
        print(f"Unexpected error with file {file_path}: {e}")
    
    return False

def filter_research_articles(source_folder, destination_folder):
    """
    Filter XML files to identify and save research articles to a separate folder.
    
    Args:
        source_folder (Path): Folder containing XML files.
        destination_folder (Path): Folder to save research articles.
    """
    # Iterate through all XML files in the source folder
    for xml_file in source_folder.glob("*.xml"):
        if is_research_article(xml_file):
            # Copy the file to the research articles folder
            destination_path = destination_folder / xml_file.name
            with open(xml_file, "r", encoding="utf-8") as src, open(destination_path, "w", encoding="utf-8") as dst:
                dst.write(src.read())
            print(f"Saved research article: {xml_file.name}")


def extract_methods(input_folder, output_folder):
    """
    Extract methods-related sections from all XML files in the 'ResearchArticles' folder.

    This function scans the 'ResearchArticles' folder for XML files, extracts sections 
    related to methods (e.g., "Methods," "Materials and Methods," "Methodology"), and saves 
    them as text files in a 'methods' subfolder.

    Returns:
        None
    """

    if not input_folder.exists():
        print(f"Input folder '{input_folder}' does not exist.")
        return

    # Iterate through XML files in the folder
    for file_path in input_folder.glob("*.xml"):
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Search for all "Methods" sections in the XML (using sec-type="methods")
            methods_sections = root.findall(".//sec[@sec-type='methods']")
            if not methods_sections:
                print(f"No section type of 'methods' found in {file_path}")
                continue

            # Find all sections with the title "Methods"
            methods_sections = root.findall(".//sec[title='Methods']")
            if not methods_sections:
                print(f"No 'Methods' section found in {file_path}")
                continue
            
            # Extract all text content from the methods sections
            methods_text = []
            for section in methods_sections:
                for element in section.iter():
                    if element.tag not in ["title", "sec"]:
                        if element.text and element.text.strip() and not element.text.strip().isdigit():
                            methods_text.append(element.text.strip().replace("\n", " "))
                        if element.tail and element.tail.strip() and not element.tail.strip().isdigit():
                            methods_text.append(element.tail.strip().replace("\n", " "))

            # Combine all extracted text into one string
            content = "\n".join(filter(None, methods_text)).strip()

            # Save the methods section to a text file
            pmc_id = file_path.name.replace(".xml", "")
            output_file = output_folder / f"methods_{pmc_id}.txt"
            with open(output_file, "w", encoding="utf-8") as txt_file:
                txt_file.write(content)
            print(f"Methods section saved to {output_file}")

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

def read_txt_files(directory):
    """
    Reads all .txt files from a specified directory.

    Args:
        directory (str): Path to the directory containing .txt files.

    Returns:
        dict: A dictionary with filenames as keys and file content as values.
    """
    txt_files = {}
    for file in os.listdir(directory):
        if file.endswith('.txt'):
            with open(os.path.join(directory, file), 'r', encoding='utf-8') as f:
                txt_files[file] = f.read().strip()
    return txt_files