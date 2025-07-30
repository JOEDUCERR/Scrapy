#We are using Bright Data API

'''
Bright data Web data platform actually scrapes the websites which have captcha
and uses a custom browser by itself to scrape the data for you

this helps as if you scrape websites with traditional methods they might ban you
or redirect you to a dummy website
'''
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

AUTH = 'brd-customer-hl_7ab40833-zone-ai_scraper:yg12kz44m8z7'
SBR_WEBDRIVER = f'https://{AUTH}@brd.superproxy.io:9515'

def scrape_website(website):
    print("Launching chrome browser...")

    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        print('Connected! Navigating...')
        driver.get(website)
        print('Taking page screenshot to file page.png')
        driver.get_screenshot_as_file('./page.png')
        print('Navigated! Scraping page content...')
        html = driver.page_source
        
        return html

#We will extract only the body content and not the html tags
def extract_body_content(html_content):
    #We use beautiful soup
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

#Now we remove all of the scripts or styles in the body content
def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    #getting all of the text seperating it with a new line
    cleaned_content = soup.get_text(separator="\n")

    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    ) #Removes unecessary \n things

    return cleaned_content

#Splitting the content into batches to help with llm token limits
def split_dom_content(dom_content, max_length=6000):
    return [ #splitting into max 6000 characters each
        dom_content[i: i + max_length] for i in range(0, len(dom_content), max_length)
    ]