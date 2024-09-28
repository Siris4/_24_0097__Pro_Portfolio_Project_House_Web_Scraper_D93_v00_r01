from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# set up the selenium driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# link to scrape from
url = 'https://www.zillow.com/sc/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22west%22%3A-85.244241453125%2C%22east%22%3A-76.608987546875%2C%22south%22%3A31.040569203933313%2C%22north%22%3A36.16170585540743%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A51%2C%22regionType%22%3A2%7D%5D%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22price%22%3A%7B%22max%22%3A250000%7D%2C%22mp%22%3A%7B%22max%22%3A1174%7D%2C%22beds%22%3A%7B%22min%22%3A2%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%2C%22sqft%22%3A%7B%22min%22%3A1250%7D%2C%22hoa%22%3A%7B%22max%22%3A50%7D%2C%22ac%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A7%2C%22usersSearchTerm%22%3A%22SC%22%7D'

# load the Zillow page
driver.get(url)
time.sleep(5)  # wait for the page to fully load


from bs4 import BeautifulSoup

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')
listings = soup.find_all('article', class_='list-card')  # extract all listings

properties = []
for listing in listings:
    try:
        address = listing.find('address', class_='list-card-addr').text
        price = listing.find('div', class_='list-card-price').text
        beds = listing.find('ul', class_='list-card-details').find_all('li')[0].text
        sqft = listing.find('ul', class_='list-card-details').find_all('li')[1].text
        year_built = listing.find('ul', class_='list-card-details').find_all('li')[2].text

        properties.append({
            'address': address,
            'price': price,
            'beds': beds,
            'sqft': sqft,
            'year_built': year_built
        })
    except:
        continue

# Close the driver after scraping
driver.quit()

# Display scraped data
import pandas as pd
df = pd.DataFrame(properties)
print(df)


import re
import pandas as pd

# Copied data from the Zillow website (this is a sample you can replace with the actual text).
zillow_data = """
SC
South Carolina Real Estate & Homes For Sale
1,456 results
5358 Carolina Hwy, Denmark, SC 29042
KELLER WILLIAMS REALTY AIKEN PARTNERS
$220,000
7 bds9 ba4,187 sqft - House for sale
Show more
Price cut: $30,000 (Sep 10)
2730 Cultra Rd., Conway, SC 29526
RE/MAX EXECUTIVE
$147,900
2 bds1 ba2,548 sqft - House for sale
Show more
4293 Brandy Creek Ct #91, Clover, SC 29710
RE/MAX LAKES & LAND, INC.
$199,900
4 bds4 ba3,272 sqft - New construction
Show more
302 West Rd, Greer, SC 29650
GIBBS REALTY & AUCTION COMPANY, Darrell Gibbs
$213,000
3 bds2 ba1,484 sqft - Foreclosure
Show more
587 Pine St, Warrenville, SC 29851
RE/MAX REINVENTED
$240,000
3 bds2 ba1,551 sqft - House for sale
Show more
217 Pleasant Dr, Greer, SC 29651
KELLER WILLIAMS REALTY
$225,000
3 bds2 ba1,266 sqft - House for sale
Show more
718 Kingsbridge Rd, Columbia, SC 29210
$249,000
4 bds3 ba2,424 sqft - House for sale
Show more
"""

# Regular expression to extract property data
property_pattern = re.compile(r'([\d,]+ [\w\s,.\']+SC \d{5})\n.*\n\$(\d{1,3}(?:,\d{3})*)\n(\d+) bds(\d+) ba([\d,]+) sqft')

matches = property_pattern.findall(zillow_data)

# Prepare property data
properties = []
for match in matches:
    address, price, beds, baths, sqft = match
    price = int(price.replace(',', ''))
    sqft = int(sqft.replace(',', ''))
    properties.append({
        'address': address,
        'price': price,
        'beds': int(beds),
        'baths': int(baths),
        'sqft': sqft
    })

# Create a DataFrame for better visualization and filtering
df = pd.DataFrame(properties)

# Print the DataFrame to view the extracted data
print(df)

# Filter the DataFrame based on criteria: minimum 2 beds and minimum 1250 sqft
filtered_df = df[(df['beds'] >= 2) & (df['sqft'] >= 1250)]
print(filtered_df)
