from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import re
from urllib.parse import urlparse, urljoin

# Set up the WebDriver options to ignore SSL certificate errors
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def is_valid_url(url):
    # Check if the URL starts with http or https
    pattern = re.compile(r'^(http|https)://')
    return re.match(pattern, url) is not None

def filter_valid_links(base_url, links):
    valid_links = []
    for link in links:
        # Check if the link is an absolute URL
        if is_valid_url(link):
            valid_links.append(link)
        else:
            # Check for relative URLs and convert to absolute
            parsed_url = urlparse(link)
            if parsed_url.scheme == '' and parsed_url.netloc == '' and parsed_url.path not in ('', '#'):
                valid_links.append(urljoin(base_url, link))
    return valid_links

def get_all_links(vals):
    all_links = []
    for val in vals:
        try:
            print(f"Processing URL: {val}")
            # Set up WebDriverWait
            wait = WebDriverWait(driver, 20)

            # Load the page
            driver.get(val)

            # Wait for the page to load completely
            wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')

            # Get the current URL
            get_url = driver.current_url

            # Check if URL is correct
            if get_url == val:
                # Get page source and parse it
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, features='html.parser')

                # Extract and filter valid links
                links = [link.get('href') for link in soup.find_all('a') if link.get('href')]
                valid_links = filter_valid_links(val, links)
                all_links.extend(valid_links)
            else:
                print(f"URL mismatch: Expected {val}, but got {get_url}")

        except TimeoutException as e:
            print(f"TimeoutException for URL: {val} - {e}")
        except Exception as e:
            print(f"An error occurred while processing {val}: {e}")

    return all_links
