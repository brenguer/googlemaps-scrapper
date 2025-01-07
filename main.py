import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class MapDataExtractor:
    def __init__(self, browser_path, driver_path):
        """
        Initialize the Selenium WebDriver with custom Chrome options.
        """
        self.browser_path = browser_path
        self.driver_path = driver_path

        # Set up Chrome options
        self.options = Options()
        self.options.binary_location = self.browser_path
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--disable-hardware-acceleration")
        self.options.add_argument("--disable-dev-shm-usage")

        # Configure WebDriver
        self.service = Service(executable_path=self.driver_path)
        self.driver = webdriver.Chrome(service=self.service, options=self.options)

        # Set explicit wait
        self.wait = WebDriverWait(self.driver, 10)

    def perform_search(self, location_query):
        """
        Open Google Maps and perform a search based on the input query.
        """
        self.driver.get("https://www.google.com/maps/")
        time.sleep(2)
        
        # Locate the search bar and input the query
        search_input = self.driver.find_element(By.ID, 'searchboxinput')
        search_input.send_keys(location_query)
        
        # Click the search button
        search_button = self.driver.find_element(By.XPATH, '//*[@id="searchbox-searchbutton"]/span')
        search_button.click()
        time.sleep(5)

    def gather_urls(self):
        """
        Scroll through the results and collect URLs of listings.
        """
        collected_links = set()
        max_scrolls = 10

        for attempt in range(max_scrolls):
            # Find all listing elements and extract their URLs
            results = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="hfpxzc"]')))
            
            for item in results:
                try:
                    link = item.get_attribute('href')
                    if link and link not in collected_links:
                        collected_links.add(link)
                except Exception as e:
                    print(f"Error while accessing link: {e}")

            # Scroll down to load more results
            scroll_container = self.driver.find_element(By.XPATH, '//*[@role="feed"]')
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scroll_container)
            time.sleep(2)

            # Break if the end of the list is reached
            if "You\'ve reached the end of the list." in self.driver.page_source:
                break

        print(f"Total URLs collected: {len(collected_links)}")
        return list(collected_links)

    def extract_details(self, urls):
        """
        Visit each URL and extract relevant information.
        """
        data = []

        for link in urls:
            try:
                self.driver.get(link)
                time.sleep(5)

                # Extract Name
                try:
                    name = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="DUwDvf lfPIob"]'))).text
                except TimeoutException:
                    name = "Unavailable"

                # Extract Phone
                try:
                    phone_elem = self.driver.find_element(By.XPATH, '//*[@class="CsEnBe" and contains(@aria-label, "Phone")]')
                    phone = phone_elem.get_attribute('aria-label').replace("Phone: ", "")
                except NoSuchElementException:
                    phone = "Unavailable"

                # Extract Website
                try:
                    website_elem = self.driver.find_element(By.XPATH, '//*[@class="CsEnBe" and contains(@aria-label, "Website")]')
                    website = website_elem.get_attribute('aria-label').replace("Website: ", "")
                except NoSuchElementException:
                    website = "Unavailable"

                # Extract Address
                try:
                    address_elem = self.driver.find_element(By.XPATH, '//*[@class="CsEnBe" and contains(@aria-label, "Address")]')
                    address = address_elem.get_attribute('aria-label').replace("Address: ", "")
                except NoSuchElementException:
                    address = "Unavailable"

                # Extract Rating
                try:
                    rating_elem = self.driver.find_element(By.XPATH, '//span[@class="ceNzKf" and @role="img"]')
                    rating = rating_elem.get_attribute('aria-label').split(' ')[0]
                except NoSuchElementException:
                    rating = "Unavailable"

                # Extract Number of Reviews
                try:
                    review_elem = self.driver.find_element(By.XPATH, '//span[contains(text(), "reviews")]')
                    reviews = review_elem.text
                except NoSuchElementException:
                    reviews = "Unavailable"

                # Append extracted data
                data.append({
                    'Name': name,
                    'Phone': phone,
                    'Website': website,
                    'Address': address,
                    'Rating': rating,
                    'Reviews': reviews
                })

            except Exception as err:
                print(f"Error processing URL {link}: {err}")

        return data

    def save_to_csv(self, dataset, output_file):
        """
        Save the extracted data to a CSV file.
        """
        dataframe = pd.DataFrame(dataset)
        dataframe.to_csv(output_file, index=False)
        print(f"Data saved to {output_file}")

    def terminate(self):
        """
        Close the WebDriver instance.
        """
        self.driver.quit()

# Main execution flow
browser_exe_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
driver_exe_path = r'C:\Users\Fenix\AppData\Local\Programs\Python\Python311\Lib\site-packages\selenium\webdriver\chromium\chromedriver.exe'

extractor = MapDataExtractor(browser_exe_path, driver_exe_path)

search_term = "machine shops in New York"
extractor.perform_search(search_term)
collected_urls = extractor.gather_urls()

# Scrape and save data
scraped_info = extractor.extract_details(collected_urls)
extractor.save_to_csv(scraped_info, 'extracted_map_data.csv')

# Close the session
extractor.terminate()
