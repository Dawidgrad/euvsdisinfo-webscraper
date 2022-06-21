from selenium.webdriver import ChromeOptions
import undetected_chromedriver as uc
from unidecode import unidecode
import datetime
import time

from source.utils import save_to_json

NUM_PAGES = 100

class Scraper:
    def __init__(self, working_dir):
        self.working_dir = working_dir
        self.options = ChromeOptions()

        # Run in headless mode
        self.options.add_argument("--headless")
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        self.options.add_argument(f'user-agent={user_agent}')

        # Create a new Chrome session
        self.driver = uc.Chrome(options=self.options)
        # self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)

    def run(self):
        links = self.get_page_links(NUM_PAGES)
        print(f'Number of links retrieved: {len(links)}\n')

        print(f'Retrieving data from links and saving to {self.working_dir}/output_data.json')
        data = []
        # Run the scraper on each link
        for link in links:
            try:
                self.get_page(link)
            except:
                self.driver.get_screenshot_as_file("error_screenshot.png")
                break

            repwidget_data = self.driver.find_element_by_class_name("b-catalog__repwidget-list").text

            # Get the relevant data
            page = {'title': unidecode(self.driver.find_element_by_class_name("b-catalog__report-title").text),
                    'summary': unidecode(self.driver.find_element_by_class_name("b-report__summary-text").text),
                    'disproof': unidecode(self.driver.find_element_by_class_name("b-report__disproof-text").text),
                    'reported_in': repwidget_data.split("REPORTED IN")[1].split("\n")[1].strip() 
                                    if "REPORTED IN" in repwidget_data else "",
                    'publication_date': repwidget_data.split("DATE OF PUBLICATION")[1].split("\n")[1].strip() 
                                        if "DATE OF PUBLICATION" in repwidget_data else "",
                    'article_language': repwidget_data.split("ARTICLE LANGUAGE(S)")[1].split("\n")[1].strip() 
                                        if "ARTICLE LANGUAGE(S)" in repwidget_data else "",
                    'regions_discussed': repwidget_data.split("REGIONS DISCUSSED IN THE DISINFORMATION")[1].split("\n")[1].strip() 
                                        if "REGIONS DISCUSSED IN THE DISINFORMATION" in repwidget_data else "",
                    'keywords': repwidget_data.split("KEYWORDS")[1].split("\n")[1].strip()
                                if "KEYWORDS" in repwidget_data else ""} 

            # Get archived links
            archived_links = []
            link_classes = self.driver.find_elements_by_class_name("b-catalog__link")

            for link_class in link_classes:
                archived_links.append(link_class.find_element_by_tag_name("span").find_element_by_tag_name("a").get_attribute("href"))

            page['archived_links'] = archived_links

            data.append(page)

        # Close the browser
        self.driver.quit()

        # Save the data to a JSON file
        save_to_json(data)
            
    # Find links in the table from the specified number of (table) pages
    def get_page_links(self, num_pages=1):
        print(f'Getting links from {num_pages} pages')
        pagelink = "https://euvsdisinfo.eu/disinformation-cases/"
        links = []

        # Go over all table pages
        for idx in range(1, num_pages + 1):
            self.get_page(pagelink)
            rows = self.driver.find_elements_by_class_name("disinfo-db-post")

            for row in rows:
                links.append(row.find_element_by_tag_name("a").get_attribute("href"))

            pagelink = f"https://euvsdisinfo.eu/disinformation-cases/?offset={idx * 10})"

        return links
    
    def get_page(self, link):
        self.driver.get(link)
        print(f'Time of the request: {datetime.datetime.now().time()}')

        # Sleep for 2 seconds to avoid rate limiting
        time.sleep(2)