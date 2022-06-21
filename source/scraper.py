from selenium import webdriver
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

from source.utils import save_to_json

NUM_PAGES = 5

class Scraper:
    def __init__(self, working_dir):
        self.working_dir = working_dir
        self.options = ChromeOptions()

        # Run in headless mode
        self.options.add_argument("--headless")
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        self.options.add_argument(f'user-agent={user_agent}')

        # Create a new Chrome session
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)

    def run(self):
        links = self.get_page_links(NUM_PAGES)
        print(f'Number of links retrieved: {len(links)}\n')

        print(f'Retrieving data from links and saving to {self.working_dir}/output_data.json')
        data = []
        # Run the scraper on each link
        for link in links:
            try:
                self.driver.get(link)
            except:
                self.driver.get_screenshot_as_file("error_screenshot.png")

            # Get the relevant data
            page = {'title': self.driver.find_element_by_class_name("b-catalog__report-title").text,
                    'summary': self.driver.find_element_by_class_name("b-report__summary-text").text,
                    'disproof': self.driver.find_element_by_class_name("b-report__disproof-text").text,
                    'repwidget': self.driver.find_element_by_class_name("b-catalog__repwidget-list").text} 
            
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
            self.driver.get(pagelink)            
            rows = self.driver.find_elements_by_class_name("disinfo-db-post")

            for row in rows:
                links.append(row.find_element_by_tag_name("a").get_attribute("href"))

            pagelink = f"https://euvsdisinfo.eu/disinformation-cases/?offset={idx * 10})"

        return links