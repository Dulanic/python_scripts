from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#import chromedriver_autoinstaller
from settings import ConfigSet
# Set chome options
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--log-level=3')
prefs = {"download.default_directory" : getattr(ConfigSet,'dl_folder')}
chrome_options.add_experimental_option("prefs",prefs)

driver = webdriver.Chrome(options=chrome_options)