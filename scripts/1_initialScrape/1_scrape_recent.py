import os
import sys
path = os.getcwd() 
package_path = (os.path.abspath(os.path.join(path, os.pardir))).replace('\\', '/')+'/'
sys.path.insert(1, package_path)
from config.config import *
from processing_scripts.raw_scrape_processing import *





url = "https://webrobots.io/kickstarter-datasets/"
scrape_url = str()



scrape_url , file_name = get_scrape_url(url)
download(scrape_url , initial_scraped_files)
unzip_data(initial_scraped_files+file_name , initial_scraped_files)

