from source.scraper import Scraper
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Arguments for the web scraping script')
    # TODO Change to use Python's default arguments
    parser.add_argument('-w', '--working_dir', help='Absolute path to the application\'s working directory', required=True)
    parser.add_argument('-l', '--links_only', help='Only get links to articles', required=False, action='store_true')
    parser.add_argument('-a', '--articles_only', help='Only scrape articles (given that links are provided in source/output/links.txt)', required=False, action='store_true')
    args = parser.parse_args()

    misinfo_classification = Scraper(args.working_dir, args.links_only, args.articles_only)
    misinfo_classification.run()