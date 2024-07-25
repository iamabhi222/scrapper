from scapper import get_content
import json
from get_links import get_all_links
from preprocessing_1 import get_sentences
from preprocessing_2 import cleaned_sentences

# def get_all_links_recursive(start_links, depth):
#     weblinks = set(start_links)
#     for _ in range(depth):
#         print("===================LEVEL=======================", _)
#         new_links = set()
#         for link in weblinks:
#             deep_links = get_all_links([link])
#             new_links.update(deep_links)
#             if len(new_links) > 100:
#                 break
#         weblinks = set(new_links)
#     return list(weblinks)

if __name__ == "__main__":
    # Initial weblinks
    # start_links = ['https://igod.gov.in/sg/states']

    # # start_links = ['https://theworldtravelguy.com/']
    
    # # Get all links recursively up to 2 levels deep
    # all_links = get_all_links_recursive(start_links, 1)

    # with open('links.json', 'w', encoding='utf-8') as file:
    #     json.dump(all_links, file, ensure_ascii=False, indent=4)


    print("====================Starting to Scrap===================")

    with open('links.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    all_links = []

# Iterate through each link in the JSON structure and add to the list
    for sector in data['Sectors']:
        cnt = 0
        for sector_name, links in sector.items():
            all_links.extend(links)
            c = c + 1
            if(c > 15):
                break

    # Scrape content from all collected links
    get_content(all_links)
    
    # Process the scraped content
    get_sentences()
    cleaned_sentences()
