from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import re

# Set up the WebDriver options to ignore SSL certificate errors
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def get_content(vals):
    # Open the file in append mode
    with open('output.txt', 'a', encoding='utf-8') as file:
        for val in vals:
            print(f"Processing URL: {val}")
            try:
                # Set up WebDriverWait
                wait = WebDriverWait(driver, 20)

                # Load the page
                driver.get(val)

                # Wait for the page to load
                wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')

                # Get the current URL
                get_url = driver.current_url

                # Check if URL is correct
                if get_url == val:
                    # Get page source and parse it
                    page_source = driver.page_source
                    soup = BeautifulSoup(page_source, 'html.parser')
                    
                    # Remove header and footer
                    for element in soup(['header', 'footer', 'nav', 'aside', 'form']):
                        element.decompose()

                    # Remove elements by class or id if necessary
                    for class_name in ['header-class', 'footer-class', 'advertisement', 'promo']:
                        for element in soup.find_all(class_=class_name):
                            element.decompose()
                    
                    for id_name in ['header-id', 'footer-id', 'ad-container', 'popup']:
                        for element in soup.find_all(id=id_name):
                            element.decompose()
                    
                    # Extract meaningful content
                    meaningful_content = []
                    for tag in soup.find_all(['article', 'main', 'section', 'div', 'p']):
                        text = tag.get_text(separator=" ", strip=True)
                        if text and not re.match(r'^\s*$', text):  # Ignore empty or whitespace-only text
                            meaningful_content.append(text)

                    # Join all extracted content
                    main_content = "\n".join(meaningful_content)

                    # Write the text to the file
                    file.write(main_content + "\n\n")  # Add two newlines for separation between pages

                else:
                    print(f"URL mismatch: Expected {val}, but got {get_url}")

            except TimeoutException as e:
                print(f"TimeoutException for URL: {val} - {e}")
            except Exception as e:
                print(f"An error occurred while processing {val}: {e}")

# Example usage
vals = ['https://example.com/page1', 'https://example.com/page2']
get_content(vals)

# Close the driver after processing
driver.quit()
