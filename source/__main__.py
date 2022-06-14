from source.scraper import Scraper
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Arguments for the web scraping script')
    # TODO Change to use Python's default arguments
    parser.add_argument('-w', '--working_dir', help='Absolute path to the application\'s working directory', required=True)
    args = parser.parse_args()

    misinfo_classification = Scraper(args.working_dir)
    misinfo_classification.run()