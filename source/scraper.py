from selenium import webdriver
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

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
        # self.driver.get_screenshot_as_file("screenshot.png")
        links = self.get_page_links()

        data = []
        # Run the scraper on each link
        for link in links:
            self.driver.get(link)

            # Get the b-catalog__report-title, b-report__summary-text, b-report__disproof-text, b-catalog__repwidget-list
            page = {'title': self.driver.find_element_by_class_name("b-catalog__report-title").text,
                    'summary': self.driver.find_element_by_class_name("b-report__summary-text").text,
                    'disproof': self.driver.find_element_by_class_name("b-report__disproof-text").text,
                    'repwidget': self.driver.find_element_by_class_name("b-catalog__repwidget-list").text} 
            
            data.append(page)

            # Close the browser
            self.driver.quit()
            
    # Find links in the table
    def get_page_links(self):
        pagelink = "https://euvsdisinfo.eu/disinformation-cases/"
        self.driver.get(pagelink)
        
        rows = self.driver.find_elements_by_class_name("disinfo-db-post")

        links = []
        for row in rows:
            links.append(row.find_element_by_tag_name("a").get_attribute("href"))

        print(f'Rows len {len(rows)}')
        print(f'Links len {len(links)}')
        print(f'Rows: {rows}')
        print(f'Links: {links}')

        # Close the browser
        self.driver.quit()

        return links