#!/usr/bin/python3

from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import getpass
import time


class SetUpBrowser():
    user_email= ''
    user_password= ''
    user_keyword= ''
    user_location= ''

    def __init__(self, webpage):
        chromedriver_path = "./chromedriver.exe"
        self.get_credentials()
        self.get_search_queries()
        self.browser = webdriver.Chrome(chromedriver_path)
        self.browser.get(webpage)

    def wait_until_element_is_visible(self, element):
        try:
            e = WebDriverWait(self.browser, 10).until(EC.visibility_of(element))
        finally:
            self.browser.quit()

    def locate_element(self, element_xpath):
        locator = self.browser.find_element_by_xpath(element_xpath)
        return locator

    def close_browser(self):
        self.browser.quit()

    def sign_in(self, email_field, password_field, signInButton_field):
        email = self.locate_element(email_field)
        password = self.locate_element(password_field)
        email.send_keys(self.user_email)
        password.send_keys(self.user_password)

        # Submit sign in after inputting credentials
        signInButton=self.locate_element(signInButton_field)
        signInButton.click()

    def get_credentials(self):
        self.user_email = input("Enter your email : ")
        self.user_password = getpass.getpass("Enter your password : ")

    def get_search_queries(self):
        self.user_keyword= input("Search (Job title, Keyword or Company): ")
        self.user_location= input("Where (City, State or Zip Code): ")   

    def perform_search(self,search_field, location_field, findJobs_field):
        # locate the input fields
        search=self.locate_element(search_field)
        location=self.locate_element(location_field)
        findJobs=self.locate_element(findJobs_field)

        # Input values
        search.send_keys(self.user_keyword)

        # This will clear all the prepopulated text in the location box
        location.send_keys(Keys.CONTROL+'a')
        location.send_keys(Keys.DELETE)
        location.send_keys(self.user_location)
        findJobs.click()

   
            


            
