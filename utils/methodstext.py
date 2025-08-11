import os
import xml.etree.ElementTree as ET
from thefuzz import fuzz

# List of section titles to match (case insensitive)
METHODS_TITLES = {"methods", "materials and methods", "methodology", "method"}

# Minimum similarity score for fuzzy matching
SIMILARITY_THRESHOLD = 80

def is_methods_section(title):
    """
    Determines if a given title matches a methods-related section
    using fuzzy string matching.

    Args:
        title (str): The section title from the XML.

    Returns:
        bool: True if the title is likely a methods section, False otherwise.
    """
    return any(fuzz.ratio(title.lower().strip(), ref) >= SIMILARITY_THRESHOLD for ref in METHODS_TITLES)

def extract_text_from_section(section):
    """
    Extracts and compiles text content from a given XML section.

    Args:
        section (ElementTree.Element): The XML <sec> element.

    Returns:
        str: Extracted text content.
    """
    section_text = []
    for elem in section.iter():
        if elem.tag not in ["title", "sec"]:  # Avoid nested sections
            if elem.text:
                section_text.append(elem.text.strip())
            if elem.tail:
                section_text.append(elem.tail.strip())
    return "\n".join(filter(None, section_text)).strip()

def extract_methods(input_folder, output_folder):
    """
    Extracts methods-related sections from full-text XML files in the given input folder
    and saves them as text files in the specified output folder.

    Args:
        input_folder (Path): Directory containing the full-text XML files.
        output_folder (Path): Directory where extracted methods will be saved.

    Returns:
        None
    """
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".xml"):
            file_path = input_folder / file_name
            try:
                tree = ET.parse(file_path)
                root = tree.getroot()

                methods_text = []
                
                # Find all <sec> sections
                for sec in root.findall(".//sec"):
                    # Check for `sec-type="methods"`
                    if sec.get("sec-type") == "methods":
                        methods_text.append(extract_text_from_section(sec))
                        continue

                    # Check section title
                    title_element = sec.find("title")
                    if title_element is not None and is_methods_section(title_element.text.strip()):
                        methods_text.append(extract_text_from_section(sec))

                # Save extracted methods
                if methods_text:
                    pmc_id = file_name.replace(".xml", "")
                    output_file = output_folder / f"methods_{pmc_id}.txt"
                    with open(output_file, "w", encoding="utf-8") as txt_file:
                        txt_file.write("\n\n".join(methods_text))
                    print(f"Extracted methods from {file_name} → {output_file}")
                else:
                    print(f"No methods section found in {file_name}")

            except Exception as e:
                print(f"Error processing file {file_name}: {e}")
