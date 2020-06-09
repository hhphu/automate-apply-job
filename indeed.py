#!/usr/bin/python3

import os
import sys
import getopt
import random
import string
import time
import getpass
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import setup
from setup import SetUpBrowser as Browser
from selenium import webdriver


indeed_url = 'https://www.indeed.com/'
signInLink_field = '//span[@class="gnav-LoggedOutAccountLink-text"]'
email_field = '//input[@id="login-email-input"]'
password_field = '//input[@id="login-password-input"]'
signInButton_field = '//button[@id="login-submit-button"]'
search_field = '//input[@id="text-input-what"]'
location_field = '//input[@id="text-input-where"]'
findJobs_field = '//button[@class="icl-Button icl-Button--primary icl-Button--md icl-WhatWhere-button"]'
job_listing_card = '//div[@class="jobsearch-SerpJobCard unifiedRow row result clickcard"]'
iframe_applyNowButton_field = '//button[@class="icl-Button icl-Button--branded icl-Button--block"]'
regular_applyNowButton_field = '//a[@class="indeed-apply-button"]'
applyCompanyButton_field = '//div[@id="applyButtonLinkContainer"]'
applyJob_iframe = '//iframe[@id="vjs-container-iframe"]'
applyModal_field = '//div[@class="indeed-apply-bd"]'

global indeed


def ApplyIndeed():
    global indeed 
    indeed= Browser(indeed_url)
    # Open the browser and go to Indeed

    indeed.browser.fullscreen_window()

    '''    
    # Go to Sign In page
    signinLink = indeed.locate_element(signInLink_field)
    signinLink.click()
    
    #Sign in
    indeed.sign_in(email_field, password_field, signInButton_field)
    time.sleep(5)
    '''
    # Peform search on Indeed
    indeed.perform_search(search_field, location_field, findJobs_field)
    indeed.browser.fullscreen_window()
    time.sleep(2)

    apply_job()

    time.sleep(10)
    indeed.close_browser()


def apply_job():

    # Get a list of job listings
    job_listing_list = indeed.browser.find_elements_by_xpath(job_listing_card)

    # Go through each job listing to apply
    for i in job_listing_list:

        # Click on the job listing. Once clicked, the listing displays an iframe where there's apply button
        i.click()
        time.sleep(3)

        isiFrame = check_iFrame()

        if (isiFrame):
            applySection = indeed.locate_element(applyJob_iframe)
            indeed.browser.switch_to_frame(applySection)
            isApplicable = check_applicability(iframe_applyNowButton_field)
            if (isApplicable):
                applyNowButton = indeed.locate_element(
                    iframe_applyNowButton_field)
                applyNowButton.click()
            else:
                break
        else:
            isApplicable = check_applicability(regular_applyNowButton_field)
            if (isApplicable):
                applyNowButton = indeed.locate_element(
                    regular_applyNowButton_field)
                applyNowButton.click()
            else:
                break


''' Some job listings require users to apply on the company's website. We'll skip these job listings.
    This function checks what apply button is displayed after clicking a job listing.
    If "Apply Now" : automate this listing
    Else: skip this listing
    Because we have 2 xpaths values for buttons within an iframe and buttons outside of an iframe, we need to pass an agurment,
'''


def check_applicability(xpath_values):
    try:
        temp = indeed.locate_element(xpath_values)
        return True
    except:
        return False


''' Some job listings use iframe in the apply section. Others don't. This function is to check if the iframe exists'''


def check_iFrame():
    try:
        temp = indeed.locate_element(applyJob_iframe)
        return True
    except:
        return False
