import pandas as pd
# from selenium import webdriver
url = 'https://support.coserv.com/hc/en-us/articles/360009093154-Standard-Residential-Rate'




# driver = webdriver.Firefox()
# driver.get(url)

# table = driver.find_element_by_xpath('//div[@class="sp5"]/table//table/..')
# table_html = table.get_attribute('innerHTML')

df = pd.read_html('https://support.coserv.com/hc/en-us/articles/360009093154-Standard-Residential-Rate')
print( df)

# driver.close()