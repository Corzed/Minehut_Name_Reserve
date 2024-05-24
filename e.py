from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import undetected_chromedriver as uc
import os
from time import sleep

chrome_profile = r'User Directory'

class ServerNameChecker:
    def __init__(self, dictionary_file_path, url, output_file):
        self.dictionary_file_path = dictionary_file_path
        self.url = url
        self.output_file = output_file
        self.driver = None
        self.available_names = []

    def setup_driver(self):
        print("Starting driver setup...")
        chrome_options = Options()
        # Uncomment the next line to run in headless mode
        # chrome_options.add_argument("--headless")
        print("Configuring Chrome options...")
        # Specifying the path to the user's Chrome profile
        user_profile_path = chrome_profile
        chrome_options.add_argument(f'user-data-dir={user_profile_path}')
        print(f"Chrome profile path set to: {user_profile_path}")

        # Initialize undetected_chromedriver with the specified options
        print("Initializing Chrome driver...")
        self.driver = uc.Chrome(options=chrome_options)
        print("Chrome driver setup completed.")

    def add_name_to_file(self, name):
        try:
            with open(self.output_file, 'a') as file:
                file.write(name + '\n')
            print(f"Name {name} added to {self.output_file}")
        except Exception as e:
            print(f"An error occurred while adding name to file: {e}")
    def enter_words(self):
        self.driver.get(self.url)
        print(f"Opened URL: {self.url}")

        # Allow the page to load completely
        sleep(5)

        try:
            with open(self.dictionary_file_path, 'r') as file:
                for line in file:
                    word = line.strip()
                    if len(word) >= 4:  # Ensure word has a minimum of 4 characters
                        # Find the input field and the check button
                        input_field = self.driver.find_element(By.CSS_SELECTOR,
                                                               'input[placeholder="Reserve Server Name..."]')
                        check_button = self.driver.find_element(By.CSS_SELECTOR, 'button.reserve-name-btn')

                        # Clear the input field, enter the word, and click the button
                        input_field.clear()
                        input_field.send_keys(word)
                        check_button.click()

                        # Wait for the response (adjust time as needed)
                        sleep(1)

                        # Check for the presence of the specific button and click it if found
                        try:
                            specific_button = self.driver.find_element(By.XPATH,
                                                                       '/html/body/div[3]/div/footer/button[2]')
                            specific_button.click()
                            print("Specific button clicked")
                            self.add_name_to_file(word)
                        except Exception as e:
                            pass
        except FileNotFoundError:
            print(f"File not found: {self.dictionary_file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.driver.quit()


if __name__ == "__main__":
    dictionary_file_path = 'words_alpha.txt'  # Update with your dictionary file path
    url = 'https://app.minehut.com/dashboard/reserve'  # Update with the actual URL
    output_file = 'available_names.txt'

    checker = ServerNameChecker(dictionary_file_path, url, output_file)
    checker.setup_driver()
    checker.enter_words()
