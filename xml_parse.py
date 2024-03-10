# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 13:52:08 2024

@author: cavsf
"""
from xml.etree import ElementTree as ET
import re




def get_category(category: str):
    file_path = 'dungeon-crawler-carl.xml'

    # Define the namespace string to use in tag searches
    ns_str = '{http://www.mediawiki.org/xml/export-0.11/}'
    # Revised approach to account for variations in the category tag
    titles = []
    category_dict={}
    
    # Make the search case-insensitive and allow for partial matches
    category_of_interest_flexible = f'[[Category:{category}'  # Note: Starting part of the category tag
    
    # Parse the XML, this time looking for a flexible match in the text content
    for event, elem in ET.iterparse(file_path, events=('end',)):
        if elem.tag == f'{ns_str}page':
            # Access the text element
            text_elem = elem.find(f'{ns_str}revision/{ns_str}text')
            if text_elem is not None and category_of_interest_flexible.lower() in text_elem.text.lower():
                # Extract the title of the page if a flexible match is found
                title = elem.find(f'{ns_str}title')
                if title is not None:
                    titles.append(title.text)
                    text_cleaned=clean_string(text_elem.text)
                    category_dict[title.text]=text_cleaned
            
            # Clear the element to free up memory
            elem.clear()
    return category_dict

def clean_string(s):
    # Remove [[Category:Something]]
    cleaned_s=s
    cleaned_s = re.sub(r'\[\[Category.*?\]\]', '', s)
    cleaned_s = re.sub(r'\{\{Spoil.*?\}\}', '', cleaned_s)
    cleaned_s = re.sub(r'\[\[File:.*?\]\]', '', cleaned_s)
    cleaned_s = re.sub(r'\[\[.*?\|(.*?)\]\]', r'\1', cleaned_s)
    cleaned_s = re.sub(r'\[\[', '', cleaned_s)
    cleaned_s = re.sub(r'\]\]', '', cleaned_s)
    cleaned_s = re.sub(r'\{\{.*?\}\}', '', cleaned_s)
    cleaned_s = re.sub(r'<ref.*?>.*?</ref>', '', cleaned_s, flags=re.DOTALL)
    cleaned_s = re.sub(r'\n+', '\n', cleaned_s)
    cleaned_s = re.sub(r'<[^>]+>', '', cleaned_s)
    cleaned_s = cleaned_s.replace("\'","")
    # Truncate after "==References=="
    # Split the string and keep only the part before "==References=="
    parts = cleaned_s.split("==References==")
    cleaned_s = parts[0] if parts else cleaned_s

    return cleaned_s
